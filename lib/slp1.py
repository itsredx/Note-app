import wmi

def watch_for_resume():
    c = wmi.WMI()
    watcher = c.watch_for(
        notification_type="Creation",
        wmi_class="Win32_PowerManagementEvent"
    )
    print("Watching for power management events...")
    while True:
        event = watcher()
        # EventType 7 corresponds to "Resume from Suspend"
        if event.EventType == 7:
            print("System has resumed from sleep.")
            # You can trigger your desired action here

if __name__ == '__main__':
    watch_for_resume()