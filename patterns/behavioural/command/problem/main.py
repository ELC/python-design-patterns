from .command import Command
from .controllers import IoTController, RemoteController
from .heating import HeatingSystem, HeatingUnit, PowerState

def main():

    heating_system = HeatingSystem([
        HeatingUnit("Bedroom"),
        HeatingUnit("Livingroom"),
        HeatingUnit("Basement"),
    ])
    assert heating_system.target_temprature_in_celcius == 22


    iot_controller = IoTController(heating_system=heating_system)
    iot_controller.add_command(Command.TURN_ON)
    iot_controller.add_command(Command.SET_TEMPERATURE, {"temperature": 24})
    iot_controller.add_command(Command.SET_TEMPERATURE, {"temperature": 26})
    iot_controller.execute()
    assert heating_system.state is PowerState.ON
    assert heating_system.target_temprature_in_celcius == 26
    
    iot_controller.undo_last_command()
    assert heating_system.target_temprature_in_celcius == 24

    iot_controller.undo_all_commands()
    assert heating_system.state is PowerState.OFF


    remote_controller = RemoteController(heating_system=heating_system)
    remote_controller.add_command(Command.TURN_ON)
    remote_controller.execute()
    assert heating_system.state is PowerState.ON

    remote_controller.add_command(Command.SET_TEMPERATURE, {"temperature": 24})
    remote_controller.execute()
    assert heating_system.target_temprature_in_celcius == 24

    remote_controller.add_command(Command.SET_TEMPERATURE, {"temperature": 26})
    remote_controller.execute()

    assert heating_system.target_temprature_in_celcius == 26
    

if __name__ == "__main__":
    main()
