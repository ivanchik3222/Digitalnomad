# event_controller.py
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from event_service import get_all_events, add_event

def events():
    events = get_all_events()
    return render_template('events.html', events=events)

@login_required
def add_event_route():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        img = request.form['image']
        author = current_user.name
        address = request.form['location']
        cost = request.form['price']
        register = request.form['register']
        add_event(title, date, description, img, author, address, cost, register)
        flash('Event added successfully!')
        return redirect(url_for('events'))
    return render_template('add_event.html')

@login_required
def add_event_form():
    return render_template('add_event.html')

def event_show(event):
    event = get_all_events()[event-1]
    return render_template('event.html',event=event)


if __name__ == '__main__':
    print("nuh uh")
else:
    print("import event_controller")