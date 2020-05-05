
let vm = new Vue({
    el: '#app',
    delimiters:["[[","]]"],
    data: {
        //v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',
        image_code_url: '',
        uuid: '',
        image_code: '',
        sms_code_tip: '獲取簡訊驗證碼',
        sms_code: '',
        send_flag: false,

        //v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,

        //error_message
        error_name_message: '',
        error_mobile_message: '',
        error_image_code_message: '',
        error_sms_code_message: '',
    },
    mounted() {  // 頁面加載完成時被調用
        this.generate_image_code();
    },
    methods: {
        // 生成圖形驗證碼獲取路徑(含UUID)
        generate_image_code() {
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';

        },
        send_sms_code() {
            if (this.send_flag == true) {
                return;
            }
            this.send_flag = true;

            this.check_mobile();
            this.check_image_code();

            if (this.error_mobile == true || this.error_image_code == true) {
                this.send_flag = false;
                return;
            }

            let url = '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        // 顯示倒數計時60秒
                        let num = 60;
                        let t = setInterval(() => {
                            if (num == 1) {
                                clearInterval(t);
                                this.sms_code_tip = '獲取簡訊驗證碼';
                                this.generate_image_code();
                                this.send_flag = false;

                            } else {
                                num -= 1;
                                this.sms_code_tip = num + '秒';
                            }
                        }, 1000)

                    } else {
                        if (response.data.code == '4001') {
                            this.error_image_code_message = response.data.errmsg;
                            this.error_image_code = true;
                        } else if (response.data.code == '4002') {
                            this.error_sms_code_message = response.data.errmsg;
                            this.error_sms_code = true;
                        }
                        this.send_flag = false;
                    }
                })
                .catch(error => {
                    console.log(error.response)
                    this.send_flag = false;
                })

        },
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name = true;
                this.error_name_message = "請輸入5-20位字符的用戶名";
            }

            // 判斷用戶名是否重複註冊
            if (this.error_name == false) {
                let url = '/usernames/' + this.username + '/count';
                axios.get(url, {
                    responseType: 'json',
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            //用戶已存在
                            this.error_name_message = '用戶已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }

                    })
                    .catch(error => {
                        console.log(error.response)
                    })
            }

        },
        check_password() {
            let re = /^[0-9a-zA-Z_-]{8,20}$/
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }

        },
        check_password2(){
            if (this.password == this.password2) {
                this.error_password2 = false;
            } else {
                this.error_password2 = true;
            }

        },
        check_mobile() {
            let re = /^09\d{8}$/
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
                this.error_mobile_message = '手機號碼格式有誤';
            }

            //判斷用戶手機是否重複
            if (this.error_mobile == false) {
                let url = '/mobiles/' + this.mobile + '/count';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            this.error_mobile_message = '手機已存在';
                            this.error_mobile = true;
                        } else {
                            this.error_mobile = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }

        },
        check_image_code() {
            if (this.image_code.length != 4) {
                this.error_image_code_message = '請輸入圖形驗證碼';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }

        },
        check_sms_code() {
            if (this.sms_code.length != 6) {
                this.error_sms_code = true;
                this.error_sms_code_message = '請填寫簡訊驗證碼';
            } else {
                this.error_sms_code = false;
            }

        },
        check_allow() {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }

        },
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_sms_code();
            this.check_allow();

            if(this.error_name == true ||
               this.error_password == true ||
               this.error_password2 == true ||
               this.error_mobile == true ||
                this.error_sms_code == true ||
               this.error_allow == true) {

                window.event.returnValue = false;
            }

        },

    }
});

