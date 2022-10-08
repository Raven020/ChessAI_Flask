jQuery(function () {

    var allMoves = [];
    var gameOver = false;
    function getAiMove(){
        var moveReq = $.get("/ai");
        
        moveReq.done(function(data){
            move = data.move;
            
            formattedMove = move.slice(0,2) +'-' + move.slice(2);
            console.log("ai move = ", formattedMove);
            board.move(formattedMove);
            moveIsValid();
            if(data.win === "true" ){
                gameWin(data.winner);
            }
            
            else if(data.check === "true"){
                $('#gameStatus').html("Status = Check");
            }
            
        })
    }

    /*
    When the onDrop function is called send attempted move to server to determine if it is valid
    */
    function onDrop (source, target, piece, newPos, oldPos, orientation) {

        allMoves.push(oldPos);
        //console.log("source = ", source, " target = ", target);
        if(!(source == target) && gameOver == false){
            sendPosition(source,target,oldPos);
        }
        else {
            return 'snapback'
        }
        

    }
    /**
     * if move is invalid Return piece to its last square
     */
    function moveIsInvalid(source, target, oldPos){
        console.log("Move is Invalid");
        //board.move(target.concat("-").concat(source));
        board.position(oldPos);
    }
    /**
     * If move is valid notify that it is the other players turn
     */
    function moveIsValid(){
        console.log("Move is Valid");
        if($('#turn').html() == "Whites Turn!"){
            $('#turn').html("Blacks Turn!");
            getAiMove();
        }
        else{
            $('#turn').html("Whites Turn!");
        }
        
    }

    function gameWin(winner){
        gameOver = true;
        $('#turn').html(winner + " Wins!")

        $('#gameStatus').html("Status = Won");
        return

    }

    /**
     * 
     * @param {*} source start square of piece
     * @param {*} target where the piece has been moved to
     */
   function sendPosition(source, target, oldPos)
    {   


        /**
         * TODO!!!
         * HIGHLIGHT LEGAL MOVES!, SEND A JSON FROM SERVER, E.G. JSON {PIECE : ARRAY_OF_LEGAL_MOVES, ETC...}
         * 
         */

        // send post request to server to verify whether move is valid
        if(target !== 'offboard'){
        var uciPos = source.concat(target)
        var req =$.post('/chess', "position=" + uciPos);
        req.done(function(data, request){
            console.log("success!");

            // if move is valid, change players turn
            if(data.win === "true" ){
                gameWin(data.winner);
            }

            else if(data.check === "true"){
                $('#gameStatus').html("Status = Check");
            }
            else{
                $('#gameStatus').html("Status = In Play");
            }


            if(data.valid === "valid"){

                moveIsValid();
            }
            // else return piece to source square
            else{
                
                moveIsInvalid(source, target, oldPos);
            }
            
        });
        req.fail(function(){
            console.log("fail");
        });
        }
    }

    var boardElement = $('#myBoard');

    var config ={
        position: 'start',
        pieceTheme :'static/img/chesspieces/wikipedia/{piece}.png',
        draggable: true,
        dropOffBoard: 'snapback',
        sparePieces: false,
        onDrop: onDrop,
       };

    
    var board = Chessboard(boardElement, config);
    //board.start;
    $('#startBtn').on('click', function(){board.start(true);
                                        $('#startBtn').html('Start Again!');
                                        gameOver = false;
                                        $.get('/chess');});
    $('#clearBtn').on('click', board.clear);

})
 