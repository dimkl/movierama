$(function(){
    /* globals $, Vue, networkManager */
    
    var app = new Vue({
        el: '#app',
        data: function(){
            return {
                movies: [],
                ordering: '-publication_date',
                createMode: false,
                username: null
            }   
        },
        mounted: function(){
            var ordering = (window.location.hash || '').replace('#', '') || this.ordering;
            this.sortMovies(ordering);
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
            updateUrl : function(fragment){
                var _hash = window.location.hash;
                var urlPath = window.location.href;
                
                if (_hash){
                    urlPath = urlPath.replace(_hash, '#'+ fragment);
                } else {
                    urlPath += '#' + fragment;
                }
                window.history.pushState('', document.title, urlPath);
            },
            // event callbacks
            sortMovies: function(ordering){
                var cmp = this;

                networkManager
                    .getUserMovies(cmp.username, ordering)
                    .then(function(response){
                        cmp.movies = response['results'];
                        cmp.ordering = ordering;
                        
                        // change url based on ordering
                        cmp.updateUrl(ordering);
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
                        cmp.username = username;
                    });
            },
            createMovie: function(movie){
                var cmp = this;
                
                networkManager
                    .createMovie(movie)
                    .then(function(response){
                        cmp.sortMovies(cmp.ordering);
                        cmp.$refs.createForm.resetData();
                    });
            },
            showCreateMovieForm : function(){
                this.createMode = !this.createMode;
            }
        }
    });
});