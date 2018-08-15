from mattermostdriver import Driver
from tools import utils, driver
import asyncio
import json


def main():

    print("Authenticating...")
    driver.login()
    driver.users.get_user('me')
    print("Successfully authenticated.")

    print("Retrieving Coffee Buddies participants...")
    team_name = 'ITTest'
    channel_name = 'town-square'
    members = utils.get_channel_members(driver, team_name, channel_name)
    print("Successfully retrieved Coffee Buddies participants.")

    print("Preparing participants database...")
    utils.create_users(members)

    driver.init_websocket(sample_handler)


@asyncio.coroutine
def sample_handler(message_string):
    """
    {
        "event": "posted",
        "data": {
            "channel_display_name":"",
            "channel_name":"a4tkpy6ifidc8pwz9pnob69yfr__oudjdi8mij8d3cuc8czumkrkpa",
            "channel_type":"D",
            "mentions":"[\"oudjdi8mij8d3cuc8czumkrkpa\"]",
            "post":"{
                    \"id\":\"kdxkhsyidb8zm8wt1nidsktqeh\",
                    \"create_at\":1534334279971,
                    \"update_at\":1534334279971,
                    \"edit_at\":0,
                    \"delete_at\":0,
                    \"is_pinned\":false,
                    \"user_id\":\"a4tkpy6ifidc8pwz9pnob69yfr\",
                    \"channel_id\":\"fxs17e67hprgmx35xabo1w98qr\",
                    \"root_id\":\"\",
                    \"parent_id\":\"\",
                    \"original_id\":\"\",
                    \"message\":\"message!\",
                    \"type\":\"\",
                    \"props\":{},
                    \"hashtags\":\"\",
                    \"pending_post_id\":\"a4tkpy6ifidc8pwz9pnob69yfr:1534334297887\"
                   }",
            "sender_name":"shadi",
            "team_id":""
        },
        "broadcast": {
            "omit_users":null,
            "user_id":"",
            "channel_id":"fxs17e67hprgmx35xabo1w98qr",
            "team_id":""
        },
        "seq": 2
    }
    """
    print(message)


if __name__ == '__main__':
    main()
