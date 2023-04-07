$(document).ready(function () {

    $("#payWithRazorpay").click(function (e) {
        console.log("checkout.js loaded successfully");
        console.log("im g=here");
        e.preventDefault();

        var first_name = $("[name='firstname']").val();
        console.log(first_name);
        var last_name = $("[name='lastname']").val();
        console.log(last_name);
        var email = $("[name='email']").val();
        console.log(email);
        var address = $("[name='selected_addresses']").val();
        console.log(address);
        var phone = $("[name='phone']").val();
        console.log(phone);
        var address_line_1 = $("[name='address_line_1']").val();
        console.log(address_line_1);
        var address_line_2 = $("[name='address_line_2']").val();
        console.log(address_line_2);
        var city = $("[name='city']").val();
        console.log(city);
        var state = $("[name='state']").val();
        console.log(state);
        var zip_code = $("[name='pincode']").val();
        console.log(zip_code);
        var token = $("[name='csrfmiddlewaretoken']").val();

        var grand_total = $("[name='grand_total']").val();
        console.log(grand_total);
        var couponCode = $("[name='couponCode']").val();
        console.log(couponCode);
        var couponDiscount = $("[name='couponDiscount']").val();
        console.log(couponDiscount);
        var amountToBePaid = $("[name='amountToBePaid']").val();
        console.log(amountToBePaid);
      
        console.log(first_name,last_name,email,phone,address_line_1,address_line_2,city,state,zip_code);


        if (
            first_name == "" ||

            last_name == "" ||
            email == "" ||
            phone == "" ||
            address_line_1 == "" ||
            address_line_2 == "" ||

            city == "" ||
            state == "" ||
            zip_code == "" 

        ) {
            swal("alert", "All fields are mandatory", "error");
            return false;
        } else {
            console.log("im in else");
            console.log(amountToBePaid);

    

            
            $.ajax({

                method: "GET",
                url:"/productapp/proceed_to_pay/",
                contentType: "application/json",
                success: function (response) {
                    console.log("im in se");

                    console.log(response, amountToBePaid);
                    var options = {
                        // key: "rzp_test_P2idDWJHzXlYX7",
                           key: e_commerce.settings.API_KEY,
                        
                        // Enter the Key ID generated from the Dashboard

                        amount: amountToBePaid *100, //response.total_price *100 , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        currency: "INR",
                        name: "Abdul musawir kp",
                        description: "Thank you",
                        // image: "",
                        handler: function (responseb) {
                            // alert(responseb.razorpay_payment_id);
                            console.log("56");
                            data = {
                                'first_name': first_name,
                                'last_name': last_name,
                                'email': email,
                                'phone': phone,
                                'address_line_1': address_line_1,
                                'address_line_2': address_line_2,
                                'city': city,
                                'state': state,
                                'selected_addresses': address,
                                'zip_code': zip_code,
                                'payment_method': "Paid by Razorpay",
                                'payment_id': responseb.razorpay_payment_id,
                                'csrfmiddlewaretoken': token,
                                'amountToBePaid': amountToBePaid,
                                'couponCode': couponCode,
                                'couponDiscount': couponDiscount,
                                'grand_total': grand_total

                            };
                            console.log(grand_total)
                            $.ajax({
                                method: "POST",
                                url: "/productapp/place_order/",
                                data: data,
                                success: function (responsec) {
                                    swal("Congratulations!", responsec.status, "success").then(
                                        (value) => {
                                            console.log("93");
                                            window.location.href =
                                                "/productapp/ordercomplete/" +
                                                "?payment_id=" +
                                                data.payment_id;
                                        }
                                    );

                                },
                            });
                            console.log("why not");
                        },
                        prefill: {

                            email: email,
                            contact: phone,
                        },
                        notes: {
                            address: "Trinity India Pvt Ltd",
                        },
                        theme: {
                            color: "#3399cc",
                        },
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                },
            });
        }
    });
})