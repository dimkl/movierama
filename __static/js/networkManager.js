(function(module){
    /* globals $, Cookies */

    /* 
        Constants
    */
    
    var RESOURCES = {
        MOVIES : '/api/movies/'
    };
    /*
        Utilities
    */
    function getCsrftoken(){
       return encodeURIComponent(Cookies.get('csrftoken'));
    }
    
    /*
        Enpoint functions
    */
    
    function createMovie(movieObj){
        var base_url = RESOURCES.MOVIES;
        return $.ajax({
            type: "POST",
            url: base_url,
            data: movieObj,
            headers: {
                "X-CSRFToken": getCsrftoken()
            },
        });
    }
    
    function getMovies(ordering){
        var base_url = RESOURCES.MOVIES;
        
        if (ordering){
            base_url += '?ordering='+ordering
        }
        
        return $.get(base_url);
    }
    
    function getUserMovies(username, ordering){
        var base_url = RESOURCES.MOVIES+'?';
        
        if (ordering){
            base_url += 'ordering='+ordering
        }
        
        if (username){
            base_url += ordering ? '&' : '' + 'search=' + username
        }
        
        return $.get(base_url);
    }
    
    function setOpinion(movie, opinion){
        var base_url = RESOURCES.MOVIES + movie+'/opinion/';
        var data =  {'opinion': opinion};
         
        return $.ajax({
            type: "POST",
            url: base_url,
            data: data,
            headers: {
                "X-CSRFToken": getCsrftoken()
            },
        });
    }
    
    /*
        Expose Api
    */
    
    module.networkManager = {
        'getMovies': getMovies,
        'getUserMovies': getUserMovies,
        'setOpinion': setOpinion,
        'createMovie': createMovie,
    };
    
})(window)