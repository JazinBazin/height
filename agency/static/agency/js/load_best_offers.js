'use strict';

var app = new Vue({
    el: '#best-offers',
    delimiters: ['[[', ']]'],
    data: {
        bestOffers: [],
        adsToShow: {},
        descriptionPageURL: "",
        tabName: "",
        currentTabIndex: 0
    },
    created() {
        var self = this;
        axios.get('best_offers/')
            .then(function (response) {
                self.bestOffers = response.data;
                if (self.bestOffers.length != 0) {
                    self.adsToShow = self.bestOffers[self.currentTabIndex].ads;
                    self.descriptionPageURL = self.bestOffers[self.currentTabIndex].description_page;
                    self.tabName = self.bestOffers[self.currentTabIndex].tab_name;
                }
            });
    },
    methods: {
        showOffers: function (event) {
            var nextTabIndex = event.target.getAttribute("data-index");

            this.adsToShow = this.bestOffers[nextTabIndex].ads;
            this.descriptionPageURL = this.bestOffers[nextTabIndex].description_page;
            this.tabName = this.bestOffers[nextTabIndex].tab_name;

            var currentPressedButton = document.getElementById('btnOpenTab' + this.currentTabIndex);
            currentPressedButton.classList.remove('focus');

            this.currentTabIndex = nextTabIndex;
        }
    }
})


Vue.component('apartment', {
    props: ['ad'],
    template: '\
            <div class= "row">\
                <div class="col text-center">{{ ad.number_of_rooms }} комнатная</div>\
                <div class="col text-center">{{ ad.floor_number }}/{{ ad.number_of_floors }} этаж</div>\
            </div>\
            '
})

Vue.component('house', {
    props: ['ad'],
    template: '\
            <div class="row">\
                <div class="col text-center">{{ ad.number_of_rooms }} комнатный</div>\
                <div class="col text-center">{{ ad.number_of_floors }} этажный</div>\
            </div>\
            '
})

Vue.component('land', {
    props: ['ad'],
    template: ''
})

Vue.component('garage', {
    props: ['ad'],
    template: ''
})

Vue.component('commercial', {
    props: ['ad'],
    template: '\
            <div class="row">\
                <div class="col text-center">{{ ad.commercial_type }}</div>\
            </div>\
            '
})