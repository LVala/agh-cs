import { loadPackageDefinition, credentials } from "@grpc/grpc-js";
import { loadSync } from "@grpc/proto-loader";
import path from "path";
import { createInterface } from "readline";

const PROTO_PATH = path.join(
  new URL(import.meta.url).pathname, 
  "../../protos/weather_notifier.proto"
);

const packageDefinition = loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });

const weatherNotifier = loadPackageDefinition(packageDefinition).weather_notifier;

const handleCall = call => {
  call.on("data", (data) => {
    console.log("--------------------");
    console.log(`City: ${data.city}`);
    console.log(`Temperature: ${data.temperature}`);
    console.log(`Sky: ${data.sky}`);
    data.falls.length ? console.log("Falls:") : console.log("No falls");
    data.falls.forEach(fall => {
      console.log(`    Type: ${fall.type}, Intensity: ${fall.intensity}`) ;
    });
    console.log("--------------------");
  });
  call.on("end", () => console.log("Connection finished"));
  call.on("error", (e) => console.error(`Connection broken: ${e}`));
  // call.on("status", (status) => console.log(`Connection returned status: ${status}`));
}

const validateArgs = (args, args_num) => {
  if (args.length < args_num) {
    console.log(`Invalid number of args, expected at least ${args_num}`);
    return true;
  }
  return false;
}

const main = () => {
  const target = process.env.ADDRESS || "localhost:50051";
  const client = new weatherNotifier.WeatherNotifier(target,
                                       credentials.createInsecure());

  const readline = createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
  });

  const calls = [];

  readline.on("line", line => {
    const args = line.split(" ");
    let sub = {};

    if (validateArgs(args, 1)) return;
    
    switch (args[0]) {
      case "periodic":
        if (validateArgs(args, 3)) return;

        sub = {interval: parseInt(args[1]), cities: args.slice(2)};
        calls.push(client.subscribePeriodic(sub));
        handleCall(calls.at(-1));
        console.log(`Subscribtion nr ${calls.length-1}`);
        break;
      case "oncond":
        if (validateArgs(args, 2)) return;
        switch (args[1]) {
          case "temperature":
            if (validateArgs(args, 4)) return;
            sub = {cities: args.slice(3), temperature: parseInt(args[2])};
            break;
          case "is_night":
            if (validateArgs(args, 4)) return;
            sub = {cities: args.slice(3), is_night: args[2] === "true"};
            break;
          case "sky":
            if (validateArgs(args, 4)) return;
            sub = {cities: args.slice(3), sky: args[2]};
            break;
          case "fall":
            if (validateArgs(args, 5)) return;
            sub = {cities: args.slice(4), fall: {type: args[2], intensity: args[3]}};
          default:
            console.log("Invalid second argument");
            return;
        }
        calls.push(client.subscribeOnCondition(sub));
        handleCall(calls.at(-1));
        console.log(`Subscribtion nr ${calls.length-1}`);
        break;
      case "cancel":
        if (validateArgs(args, 2)) return;
        calls.at(parseInt(args[1])).cancel();
        console.log(`Cancelled subscribtion nr ${args[1]}`);
        break;
      default:
        console.error("Invalid command!");
    }
  })
}

main();
