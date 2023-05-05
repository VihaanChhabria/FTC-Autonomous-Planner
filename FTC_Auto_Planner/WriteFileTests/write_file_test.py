changed = []

with open('FTC_Auto_Planner\demofile.java', 'r', encoding='utf-8') as file:
	data = file.readlines()

looper = True

while looper:
    type_movement = input("Do you want your robot to move in a direction (1), rotate in place (2), or exit (3) ? ")

    if type_movement == "1":
        #drivetrain.DrivetrainAutoMove(distance = 13, speed = 0.5, angle 270, telemetry);
        distance = input("Distance: ")
        speed = input("Speed: ")
        angle = input("Angle: ")

        changed.append(f"drivetrain.DrivetrainAutoMove({distance}, {speed}, {angle}, telemetry);")

    elif type_movement == "2":
        #DrivetrainAutoMove(double speed, double rotation, Telemetry telemetry)
        speed = input("Speed: ")
        angle = input("Angle: ")

        changed.append(f"DrivetrainAutoMove({speed}, {angle}, telemetry)")

    else:
        for movement_index, movement_value in enumerate(changed):
            data.insert(51 + movement_index, f"        {movement_value}\n")

        with open('FTC_Auto_Planner\demofile.java', 'w', encoding='utf-8') as file:
            file.writelines(data)

        looper = False

