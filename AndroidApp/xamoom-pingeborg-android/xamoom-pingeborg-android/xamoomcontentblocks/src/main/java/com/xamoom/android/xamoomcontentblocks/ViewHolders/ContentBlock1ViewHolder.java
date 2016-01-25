package com.xamoom.android.xamoomcontentblocks.ViewHolders;

import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.xamoom.android.mapping.ContentBlocks.ContentBlockType1;
import com.xamoom.android.xamoomcontentblocks.R;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * Displays audio content blocks.
 */
public class ContentBlock1ViewHolder extends RecyclerView.ViewHolder {
    private Fragment mFragment;
    private TextView mTitleTextView;
    private TextView mArtistTextView;
    private TextView mRemainingSongTimeTextView;
    private Button mPlayPauseButton;
    private MediaPlayer mMediaPlayer;
    private ProgressBar mSongProgressBar;
    private final Handler mHandler = new Handler();
    private Runnable mRunnable;

    public ContentBlock1ViewHolder(View itemView, Fragment fragment) {
        super(itemView);
        mFragment = fragment;
        mTitleTextView = (TextView) itemView.findViewById(R.id.titleTextView);
        mArtistTextView = (TextView) itemView.findViewById(R.id.artistTextView);
        mPlayPauseButton = (Button) itemView.findViewById(R.id.playPauseButton);
        mRemainingSongTimeTextView = (TextView) itemView.findViewById(R.id.remainingSongTimeTextView);
        mSongProgressBar = (ProgressBar) itemView.findViewById(R.id.songProgressBar);
    }

    public void setupContentBlock(ContentBlockType1 cb1) {
        if (cb1.getTitle() != null)
            mTitleTextView.setText(cb1.getTitle());
        else {
            mTitleTextView.setText(null);
        }

        if (cb1.getArtist() != null)
            mArtistTextView.setText(cb1.getArtist());
        else {
            mArtistTextView.setText(null);
        }

        if (cb1.getFileId() != null) {
            setupMusicPlayer(cb1);
        }
    }

    private void setupMusicPlayer(final ContentBlockType1 cb1) {
        if(mMediaPlayer == null) {
            mMediaPlayer = new MediaPlayer();

            mMediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
            try {
                mMediaPlayer.setDataSource(mFragment.getActivity(), Uri.parse(cb1.getFileId()));
                mMediaPlayer.prepareAsync();
            } catch (IOException e) {
                e.printStackTrace();
            }

            mMediaPlayer.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
                @Override
                public void onPrepared(MediaPlayer mp) {
                    mSongProgressBar.setMax(mMediaPlayer.getDuration());
                    mRemainingSongTimeTextView.setText(getTimeString(mMediaPlayer.getDuration()));

                    mPlayPauseButton.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            if (mMediaPlayer.isPlaying()) {
                                mMediaPlayer.pause();
                                mPlayPauseButton.setBackgroundResource(R.drawable.ic_play);
                            } else {
                                mMediaPlayer.start();
                                mPlayPauseButton.setBackgroundResource(R.drawable.ic_pause);
                                startUpdatingProgress();
                            }
                        }
                    });

                    mMediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                        @Override
                        public void onCompletion(MediaPlayer mp) {
                            stopUpdatingProgress();
                            if (mFragment.getActivity() != null) {
                                setupMusicPlayer(cb1);
                            }
                        }
                    });
                }
            });
        }
    }

    private String getTimeString(int milliseconds) {
        String output;

        if (TimeUnit.MILLISECONDS.toHours(milliseconds) > 0) {
            output = String.format("%02d:%02d:%02d", TimeUnit.MILLISECONDS.toHours(milliseconds),
                    TimeUnit.MILLISECONDS.toMinutes(milliseconds) % TimeUnit.HOURS.toMinutes(1),
                    TimeUnit.MILLISECONDS.toSeconds(milliseconds) % TimeUnit.MINUTES.toSeconds(1));
        } else {
            output = String.format("%02d:%02d",TimeUnit.MILLISECONDS.toMinutes(milliseconds) % TimeUnit.HOURS.toMinutes(1),
                    TimeUnit.MILLISECONDS.toSeconds(milliseconds) % TimeUnit.MINUTES.toSeconds(1));
        }

        return output;
    }

    private void startUpdatingProgress() {
        //Make sure you update Seekbar on UI thread
        mRunnable = new Runnable() {
            @Override
            public void run() {
                if (mFragment.getActivity() == null) {
                    stopUpdatingProgress();
                }

                if (mMediaPlayer != null) {
                    int mCurrentPosition = mMediaPlayer.getCurrentPosition();
                    mSongProgressBar.setProgress(mCurrentPosition);
                    mRemainingSongTimeTextView.setText(getTimeString((mMediaPlayer.getDuration() - mCurrentPosition)));
                } else {
                    mHandler.removeCallbacks(this);
                }
                mHandler.postDelayed(this, 100);
            }
        };

        mFragment.getActivity().runOnUiThread(mRunnable);
    }

    private void stopUpdatingProgress() {
        mHandler.removeCallbacks(mRunnable);
        if (mMediaPlayer != null)
            mMediaPlayer.stop();
        mPlayPauseButton.setBackgroundResource(R.drawable.ic_play);
        mSongProgressBar.setProgress(0);
    }
}