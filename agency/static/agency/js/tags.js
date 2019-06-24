'use strict';

function acres_display(value) {
    var frac = value % 1;
    if (frac == 0) {
        if (value > 20)
            value %= 10;
        if (value == 1)
            return 'сотка';
        else if (value > 0 && value < 5)
            return 'сотки';
        else
            return 'соток';
    }
    else
        return 'сотки'
}