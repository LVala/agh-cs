from generated import weather_notifier_pb2, weather_notifier_pb2_grpc 
from concurrent import futures
import random
import time
import grpc
import os

CHECK_WEATHER_INTERVAL = 1

CITIES = ["Kraków", "London", "Paris", "New York", "Tokio"]
SKIES = [
    weather_notifier_pb2.CLEAR,
    weather_notifier_pb2.PASSING_CLOUDS,
    weather_notifier_pb2.PARTLY_CLOUDY,
    weather_notifier_pb2.PASSING_CLOUDS, 
    weather_notifier_pb2.COMPLETELY_CLOUDED
]
FALLS = [
    weather_notifier_pb2.RAIN,
    weather_notifier_pb2.HAIL,
    weather_notifier_pb2.SNOW
]

INIT_TEMP = 18
INIT_IS_NIGHT = False
INIT_SKY = weather_notifier_pb2.CLEAR
INIT_FALLS = [weather_notifier_pb2.Fall(type=fall, intensity=0) for fall in FALLS]


class Weather:
    def __init__(self):
        self.weathers = {}
        for city in CITIES:
            self.weathers[city] = {
                "city": city,
                "temperature": INIT_TEMP,
                "is_night": INIT_IS_NIGHT,
                "sky": INIT_SKY,
                "falls": INIT_FALLS
            }

    def get_weather(self, city):
        if city not in CITIES: return None
         
        weather = self.weathers[city]
        weather["temperature"] =  weather["temperature"] + random.randint(-2,2)
        weather["is_night"] = not weather["is_night"] if random.randrange(100) < 10 else weather["is_night"]
        
        new_sky = random.choice(SKIES)
        weather["sky"] = weather["sky"] if random.randrange(100) < 30 else new_sky

        for fall in weather["falls"]:
            fall.intensity = min(100, max(0, fall.intensity + random.randint(-20, 10)))

        weather_resp = weather_notifier_pb2.Weather(
            city=weather["city"],
            temperature=weather["temperature"],
            is_night=weather["is_night"],
            sky=weather["sky"],
            falls=[fall for fall in weather["falls"] if fall.intensity > 0]
        )

        return weather_resp


class WeatherNotifier(weather_notifier_pb2_grpc.WeatherNotifier):
    def __init__(self):
        self.weather = Weather()

    def SubscribePeriodic(self, request, context):
        print(f"Received periodic subscribtion with interval {request.interval}, peer: {context.peer()}")
        if self._validate_cities(request.cities, context):
            return weather_notifier_pb2.Weather()

        if request.interval < 1 or request.interval > 24 * 60 * 60:
            context.set_details("Interval must in range of 1 second and 24 hours")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return weather_notifier_pb2.Weather()

        context.add_callback(lambda: print(f"Connection was lost, peer: {context.peer()}"))

        queue = []
        while True:
            for city in request.cities:
                queue.append(self.weather.get_weather(city))

            if context.is_active():
                while len(queue) > 0:
                    yield queue.pop(0)
                    print(f"Sent periodic notification, peer: {context.peer()}")

            time.sleep(request.interval)


    def SubscribeOnCondition(self, request, context):
        print(f"Received 'on condition' subscribtion, peer: {context.peer()}")
        if self._validate_cities(request.cities, context):
            return weather_notifier_pb2.Weather()

        context.add_callback(lambda: print(f"Connection was lost, peer: {context.peer()}"))
        old_weather = {city: None for city in request.cities}

        queue = []
        while True:
            for city in request.cities:
                weather = self.weather.get_weather(city)

                if old_weather[city] is None:
                    old_weather[city] = weather
                    continue

                if request.HasField("temperature"):
                    lower_to_higher = old_weather[city].temperature < request.temperature <= weather.temperature
                    higher_to_lower = weather.temperature <= request.temperature < old_weather[city].temperature
                    if lower_to_higher or higher_to_lower:
                        queue.append(weather)

                elif request.HasField("is_night"):
                    is_time_of_day = request.is_night == weather.is_night
                    was_time_of_day = request.is_night == old_weather[city].is_night
                    if is_time_of_day and not was_time_of_day:
                        queue.append(weather)

                elif request.HasField("sky"):
                    is_sky = request.sky == weather.sky
                    was_sky = request.sky == old_weather[city].sky
                    if is_sky and not was_sky:
                        queue.append(weather)
                        
                elif request.HasField("fall"):
                    for fall in weather.falls:
                        if fall.type != request.fall.type: continue

                        old_fall = weather_notifier_pb2.Fall(type=fall.type, intensity=0)
                        for old_f in old_weather[city].falls:
                            if old_f.type == request.fall.type:
                                old_fall = old_f

                        lower_to_higher = old_fall.intensity < request.fall.intensity <= fall.intensity
                        higher_to_lower = fall.intensity <= request.fall.intensity < old_fall.intensity
                        if lower_to_higher or higher_to_lower:
                            queue.append(weather)

                old_weather[city] = weather

            if context.is_active():
                while len(queue) > 0: 
                    yield queue.pop(0)
                    print(f"Sent 'on condition' notification, peer: {context.peer()}")

            time.sleep(CHECK_WEATHER_INTERVAL)

    def _validate_cities(self, cities, context):
        for city in cities:
            if city not in CITIES:
                context.set_details(f"City with name '{city}' does not exist")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return True
        return False


def serve():
    port = os.environ.get("SERVER_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_notifier_pb2_grpc.add_WeatherNotifierServicer_to_server(WeatherNotifier(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

