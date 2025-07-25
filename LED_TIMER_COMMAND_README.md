# LED Timer Command Documentation

## Overview
The LED Timer command allows you to start and stop a timer display on the LED matrix. The timer shows elapsed time in MM:SS.nnn format (minutes:seconds.milliseconds).

## Command Type
- **Type ID**: `4` (CommandTypes.LED_TIMER)
- **Command File**: `command_led_timer.py`
- **Handler Class**: `LedTimerCommand`

## Command Format

### Start Timer
```json
{
    "type": 4,
    "command_id": 1001,
    "action": "start"
}
```

### Stop Timer
```json
{
    "type": 4,
    "command_id": 1002,
    "action": "stop"
}
```

## Response Format
```json
{
    "type": 4,
    "command_id": 1001,
    "result": 1,
    "message": "LED timer started"
}
```

## Usage Examples

1. **Start the timer**:
   - Send JSON command with `"action": "start"`
   - Timer will begin displaying elapsed time on LED matrix
   - Response indicates success/failure

2. **Stop the timer**:
   - Send JSON command with `"action": "stop"`
   - Timer will stop and LED matrix will be cleared
   - Response indicates success/failure

## Display Format
- **Time Format**: MM:SS.nnn (e.g., "05:23.456")
- **Colors**: 
  - Digits: Red
  - Colon (:): Blue
  - Dot (.): Green
- **Display Area**: Uses 8x32 LED matrix horizontally

## Implementation Details
- Timer runs in a separate thread to avoid blocking the main command loop
- Timer automatically stops on system shutdown (respects THREADS_TERMINATE flag)
- LED matrix is cleared when timer stops
- Timer accuracy is approximately 50ms due to display update interval

## Error Handling
- Returns error if LED stripe hardware is not available
- Handles thread creation failures gracefully
- Provides clear error messages in response

## Dependencies
- `led_stripe.py` module for LED matrix control
- `_thread` module for background timer operation
- `machine` and `neopixel` modules (via led_stripe)
