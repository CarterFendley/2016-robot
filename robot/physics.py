from pyfrc.physics.drivetrains import four_motor_drivetrain
import wpilib

class PhysicsEngine:
    
    
    def __init__(self, controller):
        self.controller = controller
        
        # keep track of the tote encoder position
        
        # keep track of the can encoder position
        self.armAct = 500
        
    
    def update_sim(self, hal_data, now, tm_diff):
        
        # Simulate the arm
        try:
            
            armDict = hal_data['CAN'][25] # armDict is the dictionary of variables assigned to CANTalon 25
            armPercentVal = int(armDict['value']*tm_diff*2333/1023) # Encoder position increaser when in PercentVbus mode based on time and thrust value
            posVal = int(tm_diff*2333) # Encoder Position difference when in Position mode based on time
            armDict['limit_switch_closed_for'] = False 
        except:
            pass
        
        else:
            if armDict['mode_select'] == wpilib.CANTalon.ControlMode.PercentVbus: # If manual operation
                self.armAct += armPercentVal # Add the calculated encoder change value to the 'actual value'
                armDict['enc_position'] += armPercentVal # Add the calculated encoder change value to the recorded encoder value
            elif armDict['mode_select'] == wpilib.CANTalon.ControlMode.Position: #If in auto mode
                if armDict['enc_position'] < armDict['value']: #If the current position is less than the target position
                    armDict['enc_position'] += posVal # Add calculated encoder value to recorded value
                    
                else: # If the current position is more than the target position
                    armDict['enc_position'] -= posVal # Subtract calculated encoder position
            
            if self.armAct in range(-50, 50): # If the measured encoder value is within this range
                armDict['limit_switch_closed_for'] = True # Fake closing the limit switch
                
                
            armDict['enc_position'] = max(min(armDict['enc_position'], 1440), 0) # Keep encoder between these values
            
        # Simulate the drivetrain
        lf_motor = hal_data['CAN'][5]['value']*-1
        lr_motor = hal_data['CAN'][10]['value']*-1
        rf_motor = hal_data['CAN'][15]['value']*-1
        rr_motor = hal_data['CAN'][20]['value']*-1
        
        fwd, rcw = four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.controller.drive(fwd, rcw, tm_diff)