from app import App


def write_to_text_file(app: App):
    with open(r'info_for_excel.txt', 'w') as file:
        for i in range(len(app.time)):
            line = f"{app.time[i]};{app.press[i]};{app.volume[i]};{app.temperature[i]}\n"
            file.write(line)
