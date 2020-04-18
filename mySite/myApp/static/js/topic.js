var subFetch = new Vue({
    el: '#topicFetch',
    data: {
        subreddits: [],
    },
    created: function() {
        this.fetchSubredditList();
    },
    methods: {
        fetchSubredditList: function() {
            axios
            .get('/threadList/')
            .then(response => (this.subreddits = response.data.subreddits))
        console.log(this.subreddits)
        },
    },
})