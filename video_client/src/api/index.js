var fs = require('fs')
export var SERVER_URL = ''

fs.readFile('server.txt', (err, data) => {
    let b = data.toString()
    SERVER_URL = b
    debugger
})
