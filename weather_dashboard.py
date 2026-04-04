import requests
import tkinter as tk

class WeatherDashboard:
    def __init__(self, master):
        self.master = master
        master.title("Weather Dashboard")

        self.label = tk.Label(master, text="Weather Dashboard")
        self.label.pack()

        self.city_label = tk.Label(master, text="Enter city name:")
        self.city_label.pack()

        self.city_entry = tk.Entry(master)
        self.city_entry.pack()

        self.get_weather_button = tk.Button(master, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack()

        self.result_label = tk.Label(master, text="Weather info will be displayed here.")
        self.result_label.pack()

    def get_weather(self):
        city = self.city_entry.get()
        api_url = f'https://api.open-meteo.com/v1/forecast?latitude={{lat}}&longitude={{lon}}&hourly=temperature_2m,precipitation_sum&timezone=UTC'
        # Placeholder coordinates
        lat, lon = 35.6895, 139.6917  # Tokyo for example

        response = requests.get(api_url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['hourly']['temperature_2m'][0]
            precipitation = weather_data['hourly']['precipitation_sum'][0]
            self.result_label.config(text=f'Temperature: {temperature}°C, Precipitation: {precipitation}mm')
        else:
            self.result_label.config(text='Error fetching data')

if __name__ == '__main__':
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()