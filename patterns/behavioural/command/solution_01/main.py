from .command import TurnOnCommand, SetTemperatureCommand
from .controllers import IoTController, RemoteController
from .heating import HeatingSystem, HeatingUnit, PowerState

def main():

    heating_system = HeatingSystem([
        HeatingUnit("Bedroom"),
        HeatingUnit("Livingroom"),
        HeatingUnit("Basement"),
    ])
    assert heating_system.target_temprature_in_celcius == 22

    turn_on_command = TurnOnCommand(heating_system)
    set_24_degrees = SetTemperatureCommand(heating_system, 24)
    set_26_degrees = SetTemperatureCommand(heating_system, 26)


    iot_controller = IoTController[HeatingSystem]()
    iot_controller.add_command(turn_on_command)
    iot_controller.add_command(set_24_degrees)
    iot_controller.add_command(set_26_degrees)
    iot_controller.execute()
    assert heating_system.state is PowerState.ON
    assert heating_system.target_temprature_in_celcius == 26
    
    iot_controller.undo_last_command()
    assert heating_system.target_temprature_in_celcius == 24

    iot_controller.undo_all_commands()
    assert heating_system.state is PowerState.OFF


    remote_controller = RemoteController[HeatingSystem]()
    remote_controller.add_command(turn_on_command)
    remote_controller.execute()
    assert heating_system.state is PowerState.ON

    remote_controller.add_command(set_24_degrees)
    remote_controller.execute()
    assert heating_system.target_temprature_in_celcius == 24

    remote_controller.add_command(set_26_degrees)
    remote_controller.execute()

    assert heating_system.target_temprature_in_celcius == 26
    

if __name__ == "__main__":
    main()
