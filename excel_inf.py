from app import App


# Запись данных в текстовый файл
def write_to_text_file(app: App):
    filename = r'info_for_excel.txt'
    with open(filename, 'w') as file:
        for i in range(len(app.time)):
            line = f"{app.time[i]:f};{app.press[i]};{app.volume[i]};{app.temperature[i]};{app.pvt[i]}\n"
            file.write(line)
