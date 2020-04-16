var app4 = new Vue({
    el: '#app-4',
    data: {
        suggestions: [],
        seen: true,
        unseen: false,
        show: true
    },
    created: function() {
        this.fetchSuggestionList();
        this.timer = setInterval(this.fetchSuggestionList, 10000);
    },
    methods: {
        fetchSuggestionList: function() {
            axios //this is where I can pass OAuth tokens or whatever else.  Promise based lang
                .get('/suggestions/')
                // .then(response => console.log(response.data)) //for debugging
                .then(response => (this.suggestions = response.data.suggestions))
            console.log(this.suggestions)
            this.seen=false
            this.unseen=true
        },
        cancelAutoUpdate: function() {clearInterval(this.timer) }
    },
    beforeDestroy() {
        this.cancelAutoUpdate();
        //clearInterval(this.timer)
    }
  })

