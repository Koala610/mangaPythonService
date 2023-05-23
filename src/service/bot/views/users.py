from .menu_markups import create_reply_keyboard_markup, subscribe_btn, unsubscribe_btn, cng_acc_btn, menu_btn
from ..models.user import check_if_subscribed

def get_config_menu_markup(user_id):
    mark_up = create_reply_keyboard_markup() 
    subscription_btn = subscribe_btn if not check_if_subscribed(user_id) else unsubscribe_btn
    mark_up.add(
        cng_acc_btn,
        subscription_btn,
        menu_btn
    )
    return mark_up