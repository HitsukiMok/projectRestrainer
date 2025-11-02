import time
import psutil
import pygetwindow as gw
import win32gui
from datetime import datetime, timedelta
from plyer import notification

def minimize_window(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        for w in windows:
            if w.isActive:
                win32gui.ShowWindow(w._hWnd, 6)
                print(f"- Minimized {window_title}")
    except Exception:
        pass

def restrain_focus(duration_minutes, blocked_titles):
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    notified_apps = set() 

    print(f"\nRESTRAINERS ARE RUNNING")
    print(f"Bound for {duration_minutes} minutes.")
    print(f"Cannot open: {', '.join(blocked_titles)}\n")

    notification.notify(
        title="Project Restrainer:",
        message=f"You’re now bound for {duration_minutes} minutes of focus.",
        timeout=8
    )

    try:
        while datetime.now() < end_time:
            active_window = gw.getActiveWindow()
            if active_window:
                for title in blocked_titles:
                    if title.lower() in active_window.title.lower():
                        minimize_window(title)

                        if title not in notified_apps:
                            notification.notify(
                                title="Stay on track",
                                message=f"'{title}' is off-limits until your time ends.",
                                timeout=3
                            )
                            notified_apps.add(title)
                        break
            time.sleep(1)

        notification.notify(
            title="Restriction was cut.",
            message="Focus session ended.",
            timeout=10
        )
        print("\n You’ve completed your focus session.")
    
    except KeyboardInterrupt:
        print("\n Go back on track.")

if __name__ == "__main__":
    try:
        duration = int(input("Enter focus duration (minutes): "))
        titles = input("Enter window titles to block (e.g., Discord, Chrome, Spotify): ").split(",")
        titles = [t.strip() for t in titles if t.strip()]
        restrain_focus(duration, titles)
    except ValueError:
        print("Invalid input. Please enter numbers for duration.")