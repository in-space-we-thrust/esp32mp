from base_command import CommandTypes, Command
import led_stripe
import _thread
import time

class LedTimerCommand(Command):
    COMMAND_TYPE = CommandTypes.LED_TIMER
    
    def __init__(self):
        super().__init__()
        self.timer_running = False
        self.timer_thread_id = None

    def execute(self, dict_command):
        """Execute LED timer command"""
        try:
            action = dict_command.get('action', 'start')
            
            if action == 'start':
                if not self.timer_running:
                    # Start the timer in a separate thread to avoid blocking
                    self.timer_running = True
                    self.timer_thread_id = _thread.start_new_thread(self._run_timer, ())
                    result_msg = {
                        'type': dict_command['type'],
                        'command_id': dict_command.get('command_id'),
                        'result': 1,
                        'message': 'LED timer started'
                    }
                else:
                    result_msg = {
                        'type': dict_command['type'],
                        'command_id': dict_command.get('command_id'),
                        'result': 0,
                        'message': 'LED timer already running'
                    }
            
            elif action == 'stop':
                if self.timer_running:
                    self.timer_running = False
                    # Clear the LED matrix
                    led_stripe.clear_matrix()
                    led_stripe.np.write()
                    result_msg = {
                        'type': dict_command['type'],
                        'command_id': dict_command.get('command_id'),
                        'result': 1,
                        'message': 'LED timer stopped'
                    }
                else:
                    result_msg = {
                        'type': dict_command['type'],
                        'command_id': dict_command.get('command_id'),
                        'result': 0,
                        'message': 'LED timer not running'
                    }
            
            else:
                result_msg = {
                    'type': dict_command['type'],
                    'command_id': dict_command.get('command_id'),
                    'result': 0,
                    'message': f'Unknown action: {action}'
                }
                
            return result_msg
            
        except Exception as e:
            result_msg = {
                'type': dict_command['type'],
                'command_id': dict_command.get('command_id'),
                'result': 0,
                'message': f'Error: {str(e)}'
            }
            return result_msg
    
    def _run_timer(self):
        """Internal method to run the timer in a separate thread"""
        try:
            # Call the display_timer function from led_stripe.py
            # Note: We need to modify this to respect the timer_running flag
            start_time = time.ticks_ms()
            
            while self.timer_running:
                # Calculate elapsed time
                current_time = time.ticks_ms()
                elapsed_ms = time.ticks_diff(current_time, start_time)
                
                # Convert to minutes, seconds, and milliseconds
                total_seconds = elapsed_ms // 1000
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                milliseconds = elapsed_ms % 1000
                
                # Format time string MM:SS.nnn
                time_str = "{:02d}:{:02d}.{:03d}".format(minutes % 100, seconds, milliseconds)
                
                # Clear matrix
                led_stripe.clear_matrix()
                
                # Display horizontally using the 32-pixel height as width
                y_pos = 1  # Start with 1 pixel margin
                
                for i, char in enumerate(time_str):
                    if char == ':' or char == '.':
                        led_stripe.draw_char(char, 1, y_pos, led_stripe.BLUE if char == ':' else led_stripe.GREEN)
                        y_pos += 1  # 1 pixel width for separators
                    else:
                        led_stripe.draw_char(char, 1, y_pos, led_stripe.RED)
                        y_pos += 4  # 4 pixels width for digits
                
                # Update display
                led_stripe.np.write()
                
                # Small delay to prevent excessive updates
                time.sleep_ms(50)
                
        except Exception as e:
            print(f"LED timer thread error: {e}")
        finally:
            self.timer_running = False
            # Clear the display when stopping
            try:
                led_stripe.clear_matrix()
                led_stripe.np.write()
            except:
                pass
