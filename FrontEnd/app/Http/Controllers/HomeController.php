<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Luno;
use DateTime;
use App\User;
use DB;

use App\BotPlan;
use App\VolumeBot;


class HomeController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        //$this->middleware('auth');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $url = "https://bitpay.com/api/rates";
        $json =  json_decode(file_get_contents($url));

        $btc2zar = $btc2usd = $usd2zar = 0;

        foreach($json as $obj){
            if($obj->code == "ZAR") $btc2zar = $obj->rate;
            if($obj->code == "USD") $btc2usd = $obj->rate;
        }

        $usd2zar = round($btc2zar / $btc2usd , 2);

        return view('home',compact(['btc2zar', 'btc2usd', 'usd2zar']));
    }

    public function landing(){

        $url = "https://bitpay.com/api/rates";
        $json =  json_decode(file_get_contents($url));

        $btc2zar = $btc2usd = $usd2zar = 0;

        foreach($json as $obj){
            if($obj->code == "ZAR") $btc2zar = $obj->rate;
            if($obj->code == "USD") $btc2usd = $obj->rate;
        }

        $usd2zar = round($btc2zar / $btc2usd , 2);

        return view('landing',compact(['btc2zar', 'btc2usd', 'usd2zar']));
    }

    public function balance(){
        return view('balance');
    }

    public function deposit(){
        return view('deposit');
    }

    public function withdraw(){
        return view('withdraw');
    }

    public function settings(){
        $user_id = Auth::user()->id;
        $user_info = Auth::user();
        return view('settings',compact('user_id','user_info'));
    }

    public function runbot(){
        $user_id = Auth::user()->id;
        $user_info = Auth::user();

        return view('runbot',compact('user_id','user_info'));
    }

    public function botlogs(){
        $user_id = Auth::user()->id;
        $botPlans = BotPlan::where('userid',$user_id)->orderBy('id', 'DESC')->get();

        return view('botlogs',compact('botPlans'));
    }

    public function runvolumebot(){
        $user_id = Auth::user()->id;
        $user_info = Auth::user();
        return view('runvolumebot',compact('user_id','user_info'));
    }

    public function volumebotlogs(){
        $user_id = Auth::user()->id;
        $botPlans = VolumeBot::where('userid',$user_id)->orderBy('id', 'DESC')->get();

        return view('volumebotlogs',compact('botPlans'));

    }

    public function updateSettings(Request $request){
        $userId = $request->user_id;


        $apikey = $request->apikey;
        $secret = $request->secret;
        if(Auth::user()->id == $userId)
        {
            DB::table('users')
                ->where('id', $userId)
                ->update([
                    'apikey' => $apikey,
                    'secret' => $secret,
                ]);
        }

        return redirect('settings');
    }

    public function addBotPeriod(Request $request){
        $this->validate($request,
            [
                'start_date' => 'required',
                'bottype' => 'required',
                'timeFrom' => 'required',
                'timeTo' => 'required',
                'side' => 'required',
                'volume' => 'required',
                'percentage' => 'required',
                'startPrice' => 'required',
            ]);

        $dt = new DateTime;
        $created_at = $dt->format('y-m-d');

        $botplan = new BotPlan([
            'userid' => Auth::user()->id,
            'timefrom' => $request->timeFrom,
            'timeto' => $request->timeTo,
            'side' => $request->side,
            'volume' => $request->volume,
            'startprice' => $request->startPrice,
            'percentage' => $request->percentage,
            'status' => 'waiting',
            'runstate' => 1,
        ]);
        $botplan->start_date = date('Y-m-d', strtotime(str_replace('-', '/', $request->start_date)));

        $botplan->bottype = $request->bottype;


        $botplan->save();
        return redirect('/botlogs');
    }

    public function addVolumeBotPeriod(Request $request){
        $this->validate($request,
            [
                'start_date' => 'required',
                'timeFrom' => 'required',
                'timeTo' => 'required|after:timeFrom',
                'volume' => 'required',
            ]);
        $volumebot = new VolumeBot([
            'userid' => Auth::user()->id,
            'timefrom' => $request->timeFrom,
            'timeto' => $request->timeTo,
            'volume' => $request->volume,
            'status' => 'waiting',
            'runstate' => 1,
        ]);
        $volumebot->start_date = date('Y-m-d', strtotime(str_replace('-', '/', $request->start_date)));
        $volumebot->save();
        return redirect('/volumebotlogs');

    }

    public function changeBotState(Request $request){
        $state = 0;
        if ($request->bot_state == "true") {
            $state = 1;
        } elseif ($request->bot_state == "false") {
            $state = 0;
        }
        $user_id = Auth::user()->id;

        DB::table('users')
            ->where('id', $user_id)
            ->update([
                'bot_status' => $state,
            ]);
        $data = [
            'state' => $request->bot_state,
            'user_id' => $user_id
        ];
        return response()->json($data, 200);
    }

    public function changePriceBotRunState(Request $request){
        $state = 0;
        if ($request->bot_state == "true") {
            $state = 1;
        } elseif ($request->bot_state == "false") {
            $state = 0;
        }
        $botId = $request->bot_id;

        DB::table('botplans')
            ->where('id', $botId)
            ->update([
                'runstate' => $state,
            ]);
        $data = [
            'state' => $request->bot_state,
            'botid' => $botId
        ];
        return response()->json($data, 200);
    }

    public function changeVolumeBotRunState(Request $request){
        $state = 0;
        if ($request->bot_state == "true") {
            $state = 1;
        } elseif ($request->bot_state == "false") {
            $state = 0;
        }
        $botId = $request->bot_id;

        DB::table('volumebot')
            ->where('id', $botId)
            ->update([
                'runstate' => $state,
            ]);
        $data = [
            'state' => $request->bot_state,
            'botid' => $botId
        ];
        return response()->json($data, 200);
    }

    public function changePriceBotState(Request $request){
        $state = 0;
        if ($request->bot_state == "true") {
            $state = 1;
        } elseif ($request->bot_state == "false") {
            $state = 0;
        }
        $user_id = Auth::user()->id;

        DB::table('users')
            ->where('id', $user_id)
            ->update([
                'pricebot_status' => $state,
            ]);
        $data = [
            'state' => $request->bot_state,
            'user_id' => $user_id
        ];
        return response()->json($data, 200);

    }

    public function changeVolumeBotState(Request $request){
        $state = 0;
        if ($request->bot_state == "true") {
            $state = 1;
        } elseif ($request->bot_state == "false") {
            $state = 0;
        }
        $user_id = Auth::user()->id;

        DB::table('users')
            ->where('id', $user_id)
            ->update([
                'volumebot_status' => $state,
            ]);
        $data = [
            'state' => $request->bot_state,
            'user_id' => $user_id
        ];
        return response()->json($data, 200);
    }


}
