ARM_DOWN = 1
ARM_UP = 2
class PortcullisLift:
 
    def __init__(self, drive, intake, drive_speed=-.5, drive_time=5):
        self.intake = intake
        self.drive = drive
        
        self.drive_speed = drive_speed
        self.drive_time = drive_time
        
        self.is_running = False
        self.state = ARM_DOWN
    def get_running(self):
        return self.is_running
    
    def override(self):
        self.drive.set_manual()
        self.intake.set_manual(0)
        
        self.is_running = False
        
    def doit(self):
        self.is_running = True
        #Add state machine to put the arm at the bottom first
        if self.state == ARM_DOWN:
            self.intake.set_arm_bottom()
            if self.intake.on_target():
                self.state = ARM_UP
        if self.state == ARM_UP:
            self.drive.move(self.drive_speed, 0)
            self.intake.set_arm_top()
            if self.intake.on_target():
                self.is_running = False
        
    