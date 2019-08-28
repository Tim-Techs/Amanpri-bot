<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class VolumeBot extends Model
{
    protected $table = 'volumebot';
    protected $fillable = ['userid','timefrom','timeto','volume','status','start_date','runstate'];

    public function user()
    {
        return $this->belongsTo('App\User','userid');
    }


}
