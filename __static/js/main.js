$(function(){
    /* globals $, Vue, networkManager */
    
    var app = new Vue({
        el: '#app',
        data: function(){
            return {
                movies: [],
                ordering: '-publication_date',
                createMode: false
            }   
        },
        mounted: function(){
            this.sortMovies(this.ordering);
        },
        methods: {
            // utilities
            getMovieIndex: function(id){
                for (var i=0; i<this.movies.length; i++){
                    if (this.movies[i].id === id ){
                        return i;
                    }
                }
            }, 
            // event callbacks
            sortMovies: function(ordering){
                var cmp = this;

                networkManager
                    .getMovies(ordering)
                    .then(function(response){
                        cmp.movies = response['results'];
                        cmp.ordering = ordering;
                    });
            },
            setOpinion: function(movieId, opinion){
                var cmp = this;

                networkManager
                    .setOpinion(movieId, opinion)
                    .then(function(response){
                        var index = cmp.getMovieIndex(movieId);
                        cmp.movies.splice(index, 1, response)
                    });
            },
            getUserMovies: function(username){
                var cmp = this;
                
                networkManager
                    .getUserMovies(username)
                    .then(function(response){
                        cmp.movies = response['results'];
                    });
            },
            createMovie: function(movie){
                var cmp = this;
                
                networkManager
                    .createMovie(movie)
                    .then(function(response){
                        console.log(response, movie)
                        cmp.sortMovies(cmp.ordering)
                    });
            },
            showCreateMovieForm : function(){
                this.createMode = !this.createMode;
            }
        }
    });
});