const async = require("async");

function printAsync(s, cb) {
  var delay = Math.floor((Math.random() * 1000) + 500);
  setTimeout(function () {
    console.log(s);
    if (cb) cb();
  }, delay);
}
  
function task(n) {
  return new Promise((resolve, reject) => {
    printAsync(n, function () {
    resolve(n);
    });
  });
}

function loop(m) {
  const tasks = [];
  for (let i=0; i<m; ++i) {
    tasks.push((callback) => {
    console.log("RUN", i)
    task(1).then((n) => {
      console.log('task', n, 'done');
      return task(2);
    }).then((n) => {
      console.log('task', n, 'done');
      return task(3);
    }).then((n) => {
      console.log('task', n, 'done');
      console.log('done');
    }).then(() => callback(null));;
    })
  }

  async.waterfall(tasks, (err, res) => console.log(err));
}

loop(4);