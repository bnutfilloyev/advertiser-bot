from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from keyboards.inline import group_cb, post_settings, setting_cb, groups_list
from loader import dp, bot
from utils.database import MongoDB
from utils.states import Advertisement


@dp.callback_query_handler(group_cb.filter())
async def group_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['group_id'] = callback_data.get('group_id')
    await call.message.edit_text("🛠 Post sozlamalari: ", reply_markup=await post_settings())


@dp.callback_query_handler(setting_cb.filter(setting_name='get_post'))
async def get_post(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        group_id = data.get('group_id')
        post = await MongoDB.get_post(group_id)

    if post.get('message_id') is None:
        await call.message.answer("❌ Post hali yaratilmagan!")
        return

    message_id = post.get('message_id')
    chat_id = post.get('chat_id')

    await bot.copy_message(chat_id, chat_id, message_id)


@dp.callback_query_handler(setting_cb.filter(setting_name='set_post'))
async def set_post(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer("📝 Postni yuboring:")
    await Advertisement.GetAdvertisement.set()


@dp.message_handler(state=Advertisement.GetAdvertisement, content_types=ContentType.ANY)
async def get_advertisement(message: Message, state: FSMContext):
    async with state.proxy() as data:
        group_id = data.get('group_id')
        await MongoDB.set_post(group_id, message.message_id, message.chat.id)
        await message.answer("✅ Post yaratildi!")
    await state.finish()


@dp.callback_query_handler(setting_cb.filter(setting_name='back'))
async def back(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>📝 Guruhlar ro'yxati: </b>", reply_markup=await groups_list())
