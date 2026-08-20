function Dashboard() {
    let userName: string = sessionStorage.getItem("name");
    if (!userName) {
        userName = "User";
    }

    return (
        <div className="container">
            <h1>Welcome, {userName}!</h1>
        </div> 
    )
}

export default Dashboard;