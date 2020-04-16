var subFetch = new Vue({
    el: '#subFetch',
    data: {
        subreddits: [],
    },
    created: function() {
        this.fetchSubredditList();
    },
    methods: {
        fetchSubredditList: function() {
            axios
            .get('/subList/')
            .then(response => (this.subreddits = response.data.subreddits))
        console.log(this.subreddits)
        },
    },
})