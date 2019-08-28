<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class BotPlan extends Model
{
    protected $table = 'botplans';
    protected $fillable = ['userid','timefrom','timeto','side','volume','startprice','status','percentage','start_date','bottype','runstate'];

    public function user()
    {
        return $this->belongsTo('App\User','userid');
    }
}
