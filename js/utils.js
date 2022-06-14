function check(guess, answer) {
    let res = ["0","0","0","0","0"]
    let hit = [false,false,false,false,false]
    for (let i = 0; i < 5; i++) {
        if (guess[i] === answer[i]) {
            res[i] = "2"
            hit[i] = true
        }
    }

    for (let i = 0; i < 5; i++) {
        if (res[i] === "0") {
            for (let j = 0; j < 5; j++) {
                if ((guess[i] === answer[j]) && !hit[j]) {
                    res[i] = "1"
                    hit[j] = true 
                    break
                }
            }
        }
    }

    return res.join('')
}

function sum(arr) {
    return arr.reduce((a,b) => a + b)
}

function getSplits(g, C) {
    let splits = {}
    for (const res of C.map(c => check(g,c))) {
        if (!(res in splits)) splits[res] = 0
        splits[res]++
    }
    return splits
}

function v(g, C) {
    const vals = Object.entries(getSplits(g, C)).map(x => x[1])
    return [Math.max(...vals)]
}

function arrayCompare(a, b) {
    if (a.length == 0) return 0
    if (a[0] != b[0]) return a - b 
    return arrayCompare(a.slice(1), b.slice(1))
}

function compare(a, b) {
    let d = arrayCompare(a[0], b[0])
    if (d != 0) return d
    return a[1] < b[1] ? -1 : 1
}

async function getBestGuess(C) {
    if (C.length <= 2) return C[0]

    return Promise
    .all(guesses.map(async (g) => [v(g, C),g]))
    .then(values => {
        return values.sort(compare)[0][1]
    })

    
}

async function play(answer) {
    C = answers
    for (let nTurn = 1; nTurn < 20; nTurn++) {
        console.log(`Remaining ${C.length}`)

        const g = await getBestGuess(C)
        const res = check(g, answer)
        
        console.log(`Guessing ${g} --> ${res}`)
        if (res == "22222") return nTurn
        C = C.filter(c => check(g,c) == res)
    }

    return 20
}