$(function(){
    /* globals $, Vue, networkManager */
    var loc = window.location;
    var params = new URLSearchParams(loc.search)
   
    var app = new Vue({
        el: '#app',
        data: function(){
            return {
                movies: [],
                ordering: '-publication_date',
                createMode: false,
                username: params.get('search')
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
            updateUrl : function(query_key, query_value){
                params.set(query_key, query_value);
                
                var urlPath = loc.origin + loc.pathname + '?' + params.toString();
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
                        cmp.updateUrl('ordering', ordering );
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
                        cmp.updateUrl('search', username );
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