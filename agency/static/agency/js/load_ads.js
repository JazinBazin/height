'use strict';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

var app = new Vue({
    el: '#ads-list',
    delimiters: ['[[', ']]'],
    data: {
        ads: [],
        descriptionPageURL: descriptionPageURL,
        realEstateListURL: realEstateListURL,
        uniqueParamsComponentName: uniqueParamsComponentName,
        offset: 0,
        count: 1,
        adsExists: true
    },
    created() {
        this.loadAds(0, this.count);
    },
    methods: {
        submitBtnClicked: function () {
            this.ads = [];
            loadMoreAds.hidden = false;
            this.loadAds(0, this.count);
        },
        loadAdsBtnClicked: function () {
            this.loadAds(this.offset, this.count);
        },
        loadAds: function (offset, count) {
            this.switchLoadingSpinner();
            var formData = {};
            for (var i = 0; i < filtersForm.elements.length; ++i) {
                var fieldName = filtersForm.elements[i].name;
                var fieldValue = filtersForm.elements[i].value
                formData[fieldName] = fieldValue;
            }
            var self = this;
            axios.post(realEstateListURL, {
                offset: String(offset),
                count: String(count),
                formData: formData,
            }
            ).then(function (response) {
                var newAds = response.data;
                if (newAds.length < count)
                    loadingSpinner.hidden = true;
                else
                    self.switchLoadingSpinner();
                self.ads = self.ads.concat(newAds);
                self.offset = offset + newAds.length;
                self.adsExists = (self.ads.length == 0) ? false : true;
            }).catch(function (error) {
                alert("Не удалось загрузить объявления.\nПопробуйте позже.");
                self.switchLoadingSpinner();
            })
        },
        switchLoadingSpinner() {
            loadMoreAds.hidden = !loadMoreAds.hidden;
            loadingSpinner.hidden = !loadingSpinner.hidden;
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