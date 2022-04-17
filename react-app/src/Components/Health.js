export function Health(check){
    let span
    if(check.check === true){
        span =
        <span className="material-icons" style={{color: 'green'}}>
        check_circle
        </span>
    }else{
        span =
        <span className="material-icons" style={{color: 'red'}}>
        cancel
        </span>
    }
    return span
}


