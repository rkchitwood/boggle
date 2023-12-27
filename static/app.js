class Game {
    constructor(){
        this.$guessForm = $("#guess-form");
        this.$guessInput = $('#guess-form input[name="guess"]');
        this.$messageContainer = $('#messagecontainer');
        this.$scoreValue = $('#scorevalue');
        this.$timeValue = $('#timevalue');
        this.$highScore = $('#highscorevalue');

        this. guessedWords = [];
        this.score = 0;
        this.time = 60;

        this.initialize();
    }
    initialize(){
        $(document).ready(() => {
            this.$guessForm.on('submit', async (evt) => {
                //event listener on form submit to initiate checking for valid word
                evt.preventDefault();
                await this.validWordCheck(this.$guessInput.val());
                this.$guessForm[0].reset();
            });
            this.getHighScore();
            this.countDown();
        });
    }
    async validWordCheck(guess){
        //AJAX request that checks for valid word and updates the UI with the response
        const response = await axios.get('/word-check', {params: {'guess': guess}} );
        const message = response.data.replaceAll("-", " ");
        this.updateUI(message, guess);
    }
    updateUI(message, guess){
        //updates UI if word passes the validwordcheck and has not been used yet
        this.$messageContainer.text(message);
        if(message === 'ok' && !this.guessedWords.includes(guess)){
            this.guessedWords.push(guess);
            this.addScore(guess.length);
        }
    }
    addScore(points){
        //adds points equivalent to the length of the word
        this.score += points;
        this.$scoreValue.text(this.score);
    }
    countDown(){
        //function that operates the timer counting down from 60s
        this.intervalID = setInterval(() => {
            this.time -= 1;
            this.$timeValue.text(this.time);
            if(this.time === 0){
                clearInterval(this.intervalID);
                this.endGame();
            }
        }, 1000);
    }
    async endGame(){
        //deactivates the game and checks for new high score
        this.$messageContainer.html("Game Over <button><a href='/'>Restart</a></button>")
        this.$guessForm.off('submit')
        await this.highScore(this.score)
    }
    async highScore(score){
        //send score to server to check for high score
        const response = await axios.get('/high-score', {params: {'score': score}});
        if(response.data.high_score === response.data.score){
            //update high score UI
            this.$highScore.text(score);
        }
    }
    async getHighScore(){
        //gets and appends high score at startup
        const response = await axios.get('/get-high-score');
        this.$highScore.text(response.data.high_score);
    }
}

const Boggle = new Game();