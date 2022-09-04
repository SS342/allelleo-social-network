const Api_URL = "/api/v1/delete_following/"

function Delete_following(user_id, following_to, token){
    console.log("Delete_following")
     fetch(`${Api_URL}${user_id}/${following_to}/${token}`)
            .then((response) => {
                return response.json();
            });
}