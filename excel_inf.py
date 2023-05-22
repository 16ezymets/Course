import app


def write_to_excel():
    with open('excel_info', 'w') as file:
        for i in range(app.time):
            line = f"{app.time[i]};{app.press[i]};{app.temperature[i]}\n"
            file.write(line)
