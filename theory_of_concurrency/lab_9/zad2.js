const walk = require("walkdir");
const fs = require("fs");

function countLines(files, index, totalCount) {
    if (index >= files.length) {
        console.log("Total count:", totalCount)
        console.timeEnd("walk");
        return;
    };
    let count = 0;
    fs.createReadStream(files[index]).on('data', function(chunk) {
        count += chunk.toString('utf8')
        .split(/\r\n|[\n\r\u0085\u2028\u2029]/g)
        .length-1;
    }).on('end', function() {
        console.log(files[index], count);
        countLines(files, index+1, totalCount + count,);
    }).on('error', function(err) {
        countLines(files, index+1, totalCount);
    });
}

// function lc_async() {
//     console.time("walk");

//     files = walk.sync("PAM08/");
//     callbacks = files.map((filepath) => {
//         return new Promise((resolve, reject) => {
//             lines = countLines(filepath, (n) => resolve(n));
//         })
//     });

//     Promise.all(callbacks).then((result) => {
//         console.log("Lines total: ", result.reduce((acc, cur) => acc + cur, 0));
//         console.timeEnd("walk");
//     });
// }

function lc_sync() {
    console.time("walk");

    counter = 0;
    files = walk.sync("PAM08/");

    countLines(files, 0, 0);
}

lc_sync();