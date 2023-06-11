from app import App


# Запись данных в текстовый файл
def write_to_text_file(app: App):
    filename = r'info_for_excel.txt'
    with open(filename, 'w') as file:
        for i in range(len(app.time)):
            line = f"{app.time[i]:f};{app.press[i]:f};{app.volume[i]:f};{app.temperature[i]:f}\n"
            file.write(line)
