import { alertConstants } from '../_constants';

export const alertActions = {
    flash,
    clear
};

function flash(message) {
    return { type: alertConstants.FLASH, message };
}

function clear() {
    return { type: alertConstants.CLEAR };
}
