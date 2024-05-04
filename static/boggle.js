// some functions are refrence the solution to this excercise
class BoggleLogic {

    constructor(boardId, secs = 60) {
        // each round timer
        this.secs = secs;
        this.showTimer();
        //each round score
        this.score = 0;
        // update words/board
        this.words = new Set();
        this.board = $("#" + boardId);
        //set game timer
        this.timer = setInterval(this.tick.bind(this), 1000); //game timer for every 1000 millesec.

        //display word on submit click
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    // show the word that the player typed in 
    displayWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
    }

    showScore() {
        $(".score", this.board).text(this.score);
    }

    // timer update:
    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    // one second on the timer 
    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    //status messages for dom
    /* show a status message */

    showMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    //   submit button event handler: if word meets the criteria, add to score and display in record
    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Sorry you already found ${word}`, "err");
            return;
        }

        // Server validity, refrenced from solution
        const resp = await axios.get("/wordcheck", { params: { word: word } });
        if (resp.data.result === "not-word") {
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if (resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
            this.displayWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }

        $word.val("").focus();
    }

    //End Game updates
    async scoreGame() {
        $(".add-word", this.board).hide();
        const resp = await axios.post("/final-score", { score: this.score });
        if (resp.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}
