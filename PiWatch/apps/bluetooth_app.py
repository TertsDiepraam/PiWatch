import bluetooth
from pi_utils import *


def define_services():
    service = Service(
        name='bluetooth service'
    )

    @service.event_listener('bl start rfcomm server')
    @threaded
    def start_rfcomm_server(event):
        """Starts a threaded RFCOMM server, which keeps listening
            to incoming data."""
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 0
        data_size = 1024
        socket.bind(("",port))
        socket.listen(1)

        uuid = "bcfa2015-0e37-429b-8907-5b434f9b9093"
        bl_service_name = "PiWatch Android Connection Server"
        bluetooth.advertise_service(socket, bl_service_name,
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Advertising bl service: ", bl_service_name)

        try:
            client_sock, client_address = socket.accept()
            print("Accepted connection from ", client_address)
            while True:
                data = client.recv(data_size)
                if data:
                    print(data)
                    #client.send(data)
        except:
            print('Bluetooth Error: Closing socket')
            client_sock.close()
            socket.close()

    @service.event_listener('bl start rfcomm client')
    @threaded
    def start_rfcomm_client(event):
        uuid = "bcfa2015-0e37-429b-8907-5b434f9b9093"
        service_matches = bluetooth.find_service(uuid=uuid)
        if len(service_matches) == 0:
            print('No bl services found')
        else:
            match = service_matches[0]
            print('Connecting to {0}, on {1}'.format(match['name'], match['host']))
            client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            client_sock.connect(match['host'], match['port'])
            client_sock.send('Holadios!')


    @service.event_listener('bl discover')
    @threaded
    def discover_devices(event):
        print('Discovering Devices')
        try:
            nearby_devices = bluetooth.discover_devices()
        except OSError:
            print('No devices found')
            service.global_eventqueue.add(Event('bl no devices found'))
        else:
            return_value = []
            for bdaddr in nearby_devices:
                return_value.append(bluetooth.lookup_name(bdaddr))
                print('Done with Discovering')
                service.global_eventqueue.add(Event('bl discovered', data=return_value))

    return service


def define_app():
    app = App(
        name='bluetooth app'
    )
    main = Activity(
        name='main'
    )

    discover_bttn = Text(
        message='Discover Devices',
        size=30,
        position=('midtop', 0, 10),
        bg_color=(50, 50, 50),
    )

    server_bttn = Text(
        message='Start server',
        size=30,
        position=('midbottom', 0, -10),
        bg_color=(50,50,50)
    )

    discovered_devices = List(
        position=('midtop', 0, 50),
    )
    discovered_devices.add(Text(message='No Discovered Devices'))

    @main.event_listener('mouse_down')
    def mouse_down_handler(event):
        if discover_bttn.check_collision(event.pos):
            app.global_eventqueue.add(Event('bl discover'))
        if server_bttn.check_collision(event.pos):
            app.global_eventqueue.add(Event('bl start rfcomm server'))

    @app.event_listener('bl discovered')
    def bl_discovered(event):
        adapter = [str_to_text(string) for string in event.data]
        discovered_devices.clear()
        discovered_devices.add(*adapter)

    main.add(discover_bttn, server_bttn, discovered_devices)
    app.add(main)

    return app
