function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var tiles = [0, 1, 2, 3, 4, 5, 6, 7, 8];

    var renderTiles = function ($target, tiles) {
        
        var $ul = $("<ul>", {
            "class": "n-puzzle"
        });

        $(tiles).each(function (index) {
            if(tiles[index]==0){
                var $li = $("<li>", {
                    "data-tile": this,
                    "id":this,
                    "class": 'incorrect',
                });
                $li.text(this);
                $li.click({index: index}, shiftTile);
                $ul.append($li);
            }
            else{
                var $li = $("<li>", {
                    "data-tile": this,
                    "id":this,
                    "class": 'correct',
                });
                $li.text(this);
                $li.click({index: index}, shiftTile);
                $ul.append($li);
            }
        })
        $target.html($ul);
    };

    var shiftTile = function (event) {
        var index = event.data.index;
        var targetIndex = -1;
        console.log(tiles.findIndex(tile => tile === 0), index)
        if (index - 1 >= 0 && tiles[index - 1] == 0 && index % 3 != 0) { // check left
            targetIndex = index - 1;
        } else if (index + 1 < tiles.length && tiles[index + 1] == 0 && (index+1) % 3 != 0) { // check right
            console.log("That")
            targetIndex = index + 1;
        } else if (index - 3 >= 0 && tiles[index - 3] == 0) { //check up
            targetIndex = index - 3;
        } else if (index + 3 < tiles.length && tiles[index + 3] == 0) { // check down
            targetIndex = index + 3;
        }

        if (targetIndex != -1) {
            var temp = tiles[targetIndex];
            tiles[targetIndex] = tiles[index];
            tiles[index] = temp;
            renderTiles($('.eight-puzzle'), tiles);
        }

        event.preventDefault();
    };

    renderTiles($('.eight-puzzle'), tiles);

    const delay = ms => new Promise(res => setTimeout(res, ms));

    const makeMoves = async () => {
        var array1 = []
        for (var i = 0; i < solution.length; i++) {
            array1.push(parseInt(solution[i]));
            if(array1.length == 9)
            {
                renderTiles($('.eight-puzzle'), array1);
                tiles = array1
                console.log(array1)
                await delay(1000);
                array1 =[]
            }
        }
    }
    function solverFunction(){
        
        $.ajax({
            headers: { "X-CSRFToken": csrftoken },
            url: '/solve/'+tiles.join(""),
            data: {
                csrfmiddlewaretoken: csrftoken,
            },
            type: 'post',
            success: function(response){
                solution = response.solution;
                makeMoves(solution);
            },
            error: function(data){
                
            }
        })        
    };

    function randomize(){
        var newState = []
        for(var i = 0; i < 60; i++){
            var x = Math.floor((Math.random() * 8) + 1);
            console.log(x)
            document.getElementById(x).click();
        }
    }