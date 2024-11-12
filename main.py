from fastapi 										import FastAPI, Form, Cookie
from fastapi.staticfiles 				import StaticFiles
from fastapi.responses 					import FileResponse, RedirectResponse
import uvicorn
import starlette.status as status
import json
import pickle

# from db import *
from parser import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.add_middleware(AuthenticationMiddleware, backend=SomeBackend)

Error 			= ''
steam_id		= ''
img_account = ''

# main page
@app.get("/")
def main():
	# загрузка главной страницы
	return FileResponse("static/index.html")

@app.get("/sign_in")
def sign_in():
	return FileResponse('static/sign_in.html')

def SetCookie(resp, key, value):
	resp.set_cookie(key = key, value = value)

@app.post("/postdata_sign_in")
def postdata_sign_up(	Login							: str = Form(default = 'Empty'),
											Password					: str = Form(default = 'Empty')):
	
	Error = ''
	if Login != 'Empty' or Password != 'Empty':

		SignUp, steam_id, img_account, nickname = check_sign_up(Login, Password)

		if SignUp == False:
			Error = 'Data error'

	else:
		Error = 'The data entered is not complete.'

	if Error != '':
		rr = RedirectResponse('/sign_in', status_code=status.HTTP_302_FOUND)
		SetCookie(rr, 'Error', Error)

	if Error == '':
		# print('yesd')
		rr = RedirectResponse('/', status_code=status.HTTP_302_FOUND)

		SetCookie(rr, 'steamID'			, steam_id		)
		SetCookie(rr, 'img_account'	, img_account	)
		SetCookie(rr, 'nickname'		, nickname		)
		SetCookie(rr, 'login'				, Login				)
		SetCookie(rr, 'password'		, Password		)

		rr.delete_cookie('Error')
	
	return rr

@app.post("/postdata_start")
def postdata_start(	stick_1				: str 	= Form(default = 'Empty'),
										stick_2				: str 	= Form(default = 'Empty'),
										stick_3				: str 	= Form(default = 'Empty'),
										stick_4				: str 	= Form(default = 'Empty'),
										FN						: bool 	= Form(default = False	),
										MW						: bool 	= Form(default = False	),
										FT						: bool 	= Form(default = False	),
										WW						: bool 	= Form(default = False	),
										BS						: bool 	= Form(default = False	),
										select_weapon	: str 	= Form(default = 'Empty'),
										select_type		: str 	= Form(default = 'Empty'),
										min_balance		: int 	= Form(default = 0			),
										max_balance		: int 	= Form(default = 0			),
										balance				: int 	= Form(default = 0			),

										login 				: str | None = Cookie(default=None),
										password 			: str | None = Cookie(default=None)
										):

	user_steam(
		login 				, password, 
		stick_1 			, stick_2 		, stick_3 , stick_4	, 
		FN 						, MW 					, FT 			, WW  		, BS, 
		select_weapon	, select_type	, 
		min_balance		, max_balance	, balance
		)

	
	rr = RedirectResponse('/', status_code=status.HTTP_302_FOUND)

	return rr



if __name__ == '__main__':
	uvicorn.run("main:app", host="127.0.0.1", port = 8080)