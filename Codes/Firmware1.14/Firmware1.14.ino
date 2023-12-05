// Version: 1.14
// Data: Nov 11, 2023
#include <BleKeyboard.h>
#include "/Users/ws/AutismProject/SendKeyStrokes/config.h"
#if LV_USE_MSGBOX


TTGOClass *ttgo;
BleKeyboard bleKeyboard;

TFT_eSPI *tft =  nullptr;

static lv_obj_t *mbox, *info;
static lv_style_t style_modal;


static void mbox_event_cb(lv_obj_t *obj, lv_event_t evt)
{
    if(evt == LV_EVENT_DELETE && obj == mbox) {
        /* Delete the parent modal background */
        lv_obj_del_async(lv_obj_get_parent(mbox));
        mbox = NULL; /* happens before object is actually deleted! */
    } else if(evt == LV_EVENT_VALUE_CHANGED) {
        /* A button was clicked */
        lv_msgbox_start_auto_close(mbox, 0);
    }
}

static void event_handler1(lv_obj_t *obj, lv_event_t event)
{
  static int recording = 0;
  if (event == LV_EVENT_VALUE_CHANGED) {
    lv_obj_t *obj = lv_obj_create(lv_scr_act(), NULL);
    lv_obj_reset_style_list(obj, LV_OBJ_PART_MAIN);
    lv_obj_add_style(obj, LV_OBJ_PART_MAIN, &style_modal);
    lv_obj_set_pos(obj, 0, 0);
    lv_obj_set_size(obj, LV_HOR_RES, LV_VER_RES);

    static const char * btns2[] = {"Ok", ""};

    mbox = lv_msgbox_create(obj, NULL);
    lv_msgbox_add_btns(mbox, btns2);
    if(recording == 0) {
      recording = 1;
      lv_msgbox_set_text(mbox, "Recording starts.");
      
    } else {
      recording = 0;
      lv_msgbox_set_text(mbox, "Recording stops.");
    }
    lv_obj_align(mbox, NULL, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_event_cb(mbox, mbox_event_cb);

    
    
    Serial.printf("Toggled\n");
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press('r');
    delay(150);
    bleKeyboard.releaseAll();
    ttgo->motor->onec();
  }
}

static void event_handler2(lv_obj_t *obj, lv_event_t event)
{
  if (event == LV_EVENT_VALUE_CHANGED) {
    Serial.printf("Toggled\n");
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press('a');
    delay(150);
    bleKeyboard.releaseAll();
    ttgo->motor->onec();
  }
}

static void event_handler3(lv_obj_t *obj, lv_event_t event)
{
  if (event == LV_EVENT_VALUE_CHANGED) {
    Serial.printf("Toggled\n");
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press('b');
    delay(150);
    bleKeyboard.releaseAll();
    ttgo->motor->onec();
  }
}

static void event_handler4(lv_obj_t *obj, lv_event_t event)
{
  if (event == LV_EVENT_VALUE_CHANGED) {
    Serial.printf("Toggled\n");
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press('c');
    delay(150);
    bleKeyboard.releaseAll();
    ttgo->motor->onec();
  }
}

static void event_handler5(lv_obj_t *obj, lv_event_t event)
{
  if (event == LV_EVENT_VALUE_CHANGED) {
    Serial.printf("Toggled\n");
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press('d');
    delay(150);
    bleKeyboard.releaseAll();
    ttgo->motor->onec();
  }
}

static void event_handler_dropdown(lv_obj_t *obj, lv_event_t event)
{
  if (event == LV_EVENT_VALUE_CHANGED) {
    char buf[32];
    lv_dropdown_get_selected_str(obj, buf, sizeof(buf));
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press(buf[7]);
    delay(150);
    bleKeyboard.releaseAll();
    ttgo->motor->onec();
  }
}

void setup() {
  Serial.begin(115200);
  ttgo = TTGOClass::getWatch();
  ttgo->begin();
  ttgo->openBL();
  ttgo->lvgl_begin();
  ttgo->motor_begin();
  pinMode(TP_INT, INPUT);
  Serial.println("Starting BLE work");
  bleKeyboard.begin();

  lv_obj_t *label;

  /*
  lv_obj_t *label1 = lv_label_create(lv_scr_act(), NULL);
  lv_label_set_recolor(label1, true);
  lv_label_set_text(label1, "#0000ff Disconnected#");
  lv_obj_align(label1, NULL, LV_ALIGN_CENTER, 0, -70);
  */

  //b1
  lv_obj_t *btn1 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn1, event_handler1);
  lv_obj_align(btn1, NULL, LV_ALIGN_CENTER, 0, -20);
  lv_btn_set_checkable(btn1, true);
  lv_btn_set_fit2(btn1, LV_FIT_NONE, LV_FIT_TIGHT);

  label = lv_label_create(btn1, NULL);
  lv_label_set_text(label, "Record");

  //b2
  lv_obj_t *btn2 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn2, event_handler2);
  lv_obj_align(btn2, NULL, LV_ALIGN_CENTER, -30, 30);
  lv_btn_set_checkable(btn2, true);
  lv_btn_set_fit2(btn2, LV_FIT_NONE, LV_FIT_TIGHT);
  lv_obj_set_size(btn2, 90, 50);

  label = lv_label_create(btn2, NULL);
  lv_label_set_text(label, "B1");

  //b3
  lv_obj_t *btn3 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn3, event_handler3);
  lv_obj_align(btn3, NULL, LV_ALIGN_CENTER, 70, 30);
  lv_btn_set_checkable(btn3, true);
  lv_btn_set_fit2(btn3, LV_FIT_NONE, LV_FIT_TIGHT);
  lv_obj_set_size(btn3, 90, 50);

  label = lv_label_create(btn3, NULL);
  lv_label_set_text(label, "B2");

  //b4
  lv_obj_t *btn4 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn4, event_handler4);
  lv_obj_align(btn4, NULL, LV_ALIGN_CENTER, -30, 80);
  lv_btn_set_checkable(btn4, true);
  lv_btn_set_fit2(btn4, LV_FIT_NONE, LV_FIT_TIGHT);
  lv_obj_set_size(btn4, 90, 50);

  label = lv_label_create(btn4, NULL);
  lv_label_set_text(label, "B3");

  //b5
  lv_obj_t *btn5 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn5, event_handler5);
  lv_obj_align(btn5, NULL, LV_ALIGN_CENTER, 70, 80);
  lv_btn_set_checkable(btn5, true);
  lv_btn_set_fit2(btn5, LV_FIT_NONE, LV_FIT_TIGHT);
  lv_obj_set_size(btn5, 90, 50);

  label = lv_label_create(btn5, NULL);
  lv_label_set_text(label, "B4");

  //dropdown
  /*Create a normal drop down list*/
  lv_obj_t *dd = lv_dropdown_create(lv_scr_act(), NULL);
  lv_dropdown_set_options(dd, "Subject0\n"
                          "Subject1\n"
                          "Subject2\n"
                          "Subject3\n"
                          "Subject4\n"
                          "Subject5\n"
                          "Subject6\n"
                          "Subject7\n"
                          "Subject8\n"
                          "Subject9");
  lv_obj_set_event_cb(dd, event_handler_dropdown);
  lv_obj_align(dd, NULL, LV_ALIGN_CENTER, 0, -70);
}

void loop() {
  lv_obj_t *label1 = lv_label_create(lv_scr_act(), NULL);
  lv_label_set_recolor(label1, true);
  
  
  if(bleKeyboard.isConnected()) {
    lv_label_set_text(label1, "#0000ff Connected#");
  } else{
    lv_label_set_text(label1, "#ff0000 Disconnected#");
  }
  lv_obj_align(label1, NULL, LV_ALIGN_CENTER, 0, -100);
  
  lv_task_handler();
  delay(5);
  lv_obj_del(label1);
  /*if(bleKeyboard.isConnected()) {
    Serial.println("Sending 'Hello world'...");
    bleKeyboard.print("Hello world");

    delay(1000);

    Serial.println("Sending Enter key...");
    bleKeyboard.write(KEY_RETURN);

    delay(1000);

    Serial.println("Sending Play/Pause media key...");
    bleKeyboard.write(KEY_MEDIA_PLAY_PAUSE);

    delay(1000);

    Serial.println("Sending Ctrl+Alt+Delete...");
    bleKeyboard.press(KEY_LEFT_CTRL);
    bleKeyboard.press(KEY_LEFT_ALT);
    bleKeyboard.press(KEY_DELETE);
    delay(100);
    bleKeyboard.releaseAll();
    
  }

  Serial.println("Waiting 5 seconds...");
  delay(5000);
  */
}

#endif
