
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

        //v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,

        //error_message
        error_name_message: '',
        error_mobile_message: '',
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
            this.check_allow();

            if(this.error_name == true ||
               this.error_password == true ||
               this.error_password2 == true ||
               this.error_mobile ==true ||
               this.error_allow == true) {

                window.event.returnValue = false;
            }

        },

    }
});

