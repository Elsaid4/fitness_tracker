from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.models import Follow
from fitness.forms import TrainingPlanForm, WorkoutInlineFormSet
from .models import TrainingPlan, Workout, Set, Exercise, WorkoutExercise
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

@login_required
def dashboard(request):
    if request.user.is_coach():
        plans = TrainingPlan.objects.filter(coach=request.user).order_by('-created_at')
        workouts = []
        for p in plans:
            workouts.extend(Workout.objects.filter(plan=p))

        return render(request, 'fitness/dashboard.html', {
            'user': request.user, 
            'workouts': workouts, 
            'plans': plans
            })
    else:
        workouts = Workout.objects.filter(user=request.user).order_by('-timestamp')
        workout_exercises = []
        sets = []
        for w in workouts:
            workout_exercises.extend(WorkoutExercise.objects.filter(workout=w))

        for we in workout_exercises:
            sets.extend(Set.objects.filter(workout_exercise=we))

        return render(request, 'fitness/dashboard.html', {
            'user': request.user, 
            'workouts': workouts, 
            'exercises': workout_exercises, 
            'sets': sets
            })

class PlanDetailView(LoginRequiredMixin, DetailView):
    model = TrainingPlan
    template_name = 'fitness/plan_detail.html'
    context_object_name = 'plan'


@login_required
def create_plan_view(request):
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        formset = WorkoutInlineFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                plan = form.save(commit=False)
                plan.coach = request.user
                plan.save()
                
                formset.instance = plan
                workouts = formset.save(commit=False)
                
                for workout in workouts:
                    workout.user = request.user 
                    workout.is_template = True
                    workout.save()
            
            return redirect('plan_detail', pk=plan.pk)
    else:
        form = TrainingPlanForm()
        formset = WorkoutInlineFormSet()
        
    return render(request, 'fitness/plan_create.html', {
        'form': form,
        'formset': formset
    })

User = get_user_model()
class CoachListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'fitness/coach_list.html'
    context_object_name = 'coaches'  

    def get_queryset(self):
        queryset = User.objects.filter(role='coach')
        
        scelta_filtro = self.request.GET.get('filter')
        
        if scelta_filtro == 'following' and self.request.user.is_authenticated:
            queryset = queryset.filter(followers__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            followed_coaches_ids = self.request.user.following.values_list('coach_id', flat=True)
            context['followed_coaches_ids'] = list(followed_coaches_ids)
        
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context

class CoachDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'fitness/coach_detail.html'
    context_object_name = 'coach'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coach = self.get_object()
        
        context['plans'] = TrainingPlan.objects.filter(coach=coach).prefetch_related('workouts')
        context['single_workouts'] = Workout.objects.filter(user=coach, plan__isnull=True, is_template=True)
        if self.request.user.is_authenticated:
            context['is_following'] = Follow.objects.filter(user=self.request.user, coach=coach).exists()
        else:
            context['is_following'] = False     
        return context

@login_required
def toggle_follow_view(request, coach_id):
    coach = get_object_or_404(User, id=coach_id, role='coach')
    
    if coach == request.user:
        return redirect('coach_list')

    (follow_relation, created) = Follow.objects.get_or_create(user=request.user, coach=coach)

    if not created:
        follow_relation.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'coach_list'))

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'fitness/workout_detail.html'
    context_object_name = 'workout'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.get_object()
        
        workout_exercises = WorkoutExercise.objects.filter(workout=workout)
        
        sets_by_exercise = {}
        for we in workout_exercises:
            sets_by_exercise[we] = Set.objects.filter(workout_exercise=we)
            
        context['workout_exercises'] = workout_exercises
        context['sets_by_exercise'] = sets_by_exercise
        return context



@login_required
def workout_view(request):
    workout = Workout(name=f'Workout di {request.user} - {timezone.now().strftime("%d-%m-%Y %H:%M:%S")}')
    exercises = []
    all_exercises = Exercise.objects.all()
    total_weight = 0
    

    return render(request, 'fitness/workout.html', {
        'workout': workout, 
        'exercises': exercises, 
        'all_exercises': all_exercises, 
        'tot_weight': total_weight 
    })

@login_required
def save_workout(request, workout_name):
    if request.method == 'POST':
        current_user = request.user
        duration_str = request.POST.get('workout_duration', '00:00:00')
        
        workout = Workout.objects.create(
            name=workout_name, 
            user=current_user,
            duration=duration_str
        )
        if current_user.is_coach():
            workout.is_template = True
        # Ottieni tutti gli indici degli esercizi inviati
        exercise_indices = [k.split('_')[1] for k in request.POST.keys() if '_name' in k]

        for i in exercise_indices:
            exercise_name = request.POST.get(f'exercise_{i}_name')
            exercise_obj = Exercise.objects.get(name=exercise_name)

            workout_exercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise_obj)
            
            reps_list       = request.POST.getlist(f'exercise_{i}_reps[]')
            weights_list    = request.POST.getlist(f'exercise_{i}_weight[]')
            completed_list  = request.POST.getlist(f'exercise_{i}_completed[]')
            
            for reps, weight, completed in zip(reps_list, weights_list, completed_list):
                is_completed = completed == "true"
                Set.objects.create(
                    workout_exercise    = workout_exercise,
                    repetitions         = reps,
                    weight              = weight,
                    completed           = is_completed
                )
        return redirect('workout_detail', pk=workout.id)
    return redirect('dashboard')