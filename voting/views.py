from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count  # ← Important for counting votes
from .models import VotingStatus, AdminUser, Voter, Candidate, Vote

def homepage(request):
    try:
        status = VotingStatus.objects.get(id=1)
    except VotingStatus.DoesNotExist:
        status = VotingStatus.objects.create(id=1, is_voting_active=False)

    if request.method == 'POST' and 'cast_vote' in request.POST:
        if not status.is_voting_active:
            return HttpResponse("<script>alert('Voting has not started yet');window.location.href='/';</script>")
        return redirect('cast_vote')

    return render(request, 'voting/homepage.html', {'voting_status': status})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            admin = AdminUser.objects.get(username=username, password=password)
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, 'voting/admin_login.html')

def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    return render(request, 'voting/admin_dashboard.html')

def total_votes(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    # Count votes per candidate
    votes = Vote.objects.values('candidate__name').annotate(count=Count('id'))
    total_votes = Vote.objects.count()

    return render(request, 'voting/total_votes.html', {'votes': votes, 'total_votes': total_votes})

def edit_candidates(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    voting_status = VotingStatus.objects.get(id=1)
    if voting_status.is_voting_active or Vote.objects.exists():
        return HttpResponse("<script>alert('Current voting must be reset before editing');window.location.href='/admin_dashboard';</script>")

    candidates = Candidate.objects.all()

    if request.method == 'POST':
        if 'add_candidate' in request.POST:
            new_candidate = request.POST['new_candidate'].strip()
            if new_candidate and new_candidate.isalpha():
                Candidate.objects.get_or_create(name=new_candidate)
                messages.success(request, 'Candidate added successfully')
            else:
                messages.error(request, 'Candidate name must contain only letters')
        elif 'remove_candidate' in request.POST:
            candidate_id = request.POST['candidate_id']
            Candidate.objects.filter(id=candidate_id).delete()
            messages.success(request, 'Candidate removed successfully')
        elif 'start_voting' in request.POST:
            if Candidate.objects.count() < 2:
                return HttpResponse("<script>alert('Add minimum 2 candidates');window.location.href='/edit_candidates';</script>")
            voting_status.is_voting_active = True
            voting_status.save()
            messages.success(request, 'Voting started successfully')
            return redirect('admin_dashboard')

    return render(request, 'voting/edit_candidates.html', {'candidates': candidates})

def reset_vote(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == 'POST':
        Voter.objects.all().delete()
        Candidate.objects.all().delete()
        Vote.objects.all().delete()
        voting_status = VotingStatus.objects.get(id=1)
        voting_status.is_voting_active = False
        voting_status.save()
        messages.success(request, 'Voting reset successfully')
        return redirect('admin_dashboard')

    return render(request, 'voting/admin_dashboard.html')

def cast_vote(request):
    if not VotingStatus.objects.get(id=1).is_voting_active:
        return HttpResponse("<script>alert('Voting has not started yet');window.location.href='/';</script>")

    if request.method == 'POST':
        voter_name = request.POST['voter_name'].strip()
        if not voter_name.isalpha():
            return HttpResponse("<script>alert('Name must contain only letters and no spaces');window.location.href='/cast_vote';</script>")

        if Voter.objects.filter(name=voter_name).exists():
            return HttpResponse("<script>alert('This name has already voted');window.location.href='/cast_vote';</script>")

        voter = Voter.objects.create(name=voter_name)
        request.session['voter_id'] = voter.id
        return redirect('vote_candidate')

    return render(request, 'voting/cast_vote.html')

def vote_candidate(request):
    if not VotingStatus.objects.get(id=1).is_voting_active:
        return HttpResponse("<script>alert('Voting has not started yet');window.location.href='/';</script>")

    candidates = Candidate.objects.all()

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        voter_id = request.session.get('voter_id')
        if not candidate_id or not voter_id:
            return HttpResponse("<script>alert('Invalid selection');window.location.href='/vote_candidate';</script>")

        try:
            voter = Voter.objects.get(id=voter_id)
            candidate = Candidate.objects.get(id=candidate_id)
            Vote.objects.create(voter=voter, candidate=candidate)
            del request.session['voter_id']
            return HttpResponse("<script>alert('Vote Casted Successfully');window.location.href='/';</script>")
        except (Voter.DoesNotExist, Candidate.DoesNotExist):
            return HttpResponse("<script>alert('Invalid voter or candidate');window.location.href='/vote_candidate';</script>")

    return render(request, 'voting/vote_candidate.html', {'candidates': candidates})
